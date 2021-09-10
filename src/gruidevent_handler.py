# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles gruid events. Generates gruid events with matrix time series for a set of GEMC hits.
"""

import copy
import math
import numpy # NOTE: We could do without numpy...
import sys
from operator import itemgetter

import constants as c

def _gen_ts(hits, deltax, deltay, deltaz, dt, dx, dy, dz):
    """
    Generates a time series of sparse 2-dimensional or 3-dimensional matrices from a list of hits.
    :param hits:      list of hits in the output format of the extract_hits() method.
    :param deltax:    how much the entire detector is shifted from the x axis. Used to obtain the
                      size of the generated matrices.
    :param deltay:    how much the entire detector is shifted from the y axis. Used to obtain the
                      size of the generated matrices.
    :param deltaz:    how much the entire detector is shifted from the z axis. Used to obtain the
                      size of the generated matrices.
    :param dt:        delta t for the time series.
    :param dx:        size of the matrices' columns. Doesn't need to divide the total x size of the
                      detector.
    :param dy:        size of the matrices' rows. Doesn't need to divide the total y size of the
                      detector.
    :param dz:        size of the matrices' depth columns. Doesn't need to divide the total z size
                      of the detector. If this is NaN, no depth processing is done.
    :return:          a dictionary of 2-dimensional sparse matrices. Each matrix is defined as a
                      dictionary where a key is a tuple describing position and a value is the
                      energy deposited in eV. To further reduce storage use, if not hits are found
                      for a specific t, that t isn't event stored in the time series.
    """
    if not hits: return None
    chits = copy.deepcopy(hits) # Deep copy hits to avoid damaging original dictionary.

    tseries = {}
    max_t = 0.
    for t in chits[c.S_T]:
        if t > max_t: max_t = t

    for t in numpy.arange(0., max_t, dt):
        hitstored = False
        phits = {}

        for hi in range(len(chits[c.S_N])-1, -1, -1):
            # Check if hit is in dt.
            if t > chits[c.S_T][hi] or t+dt <= chits[c.S_T][hi]: continue

            # Store hit's position.
            sx = None
            for x in numpy.arange(-deltax, deltax+dx, dx):
                if x <= chits[c.S_X][hi] and chits[c.S_X][hi] < x+dx: sx = x
            sy = None
            for y in numpy.arange(-deltay, deltay+dy, dy):
                if y <= chits[c.S_Y][hi] and chits[c.S_Y][hi] < y+dy: sy = y
            sz = 0
            if not math.isnan(dz):
                sz = None
                for z in numpy.arange(-deltaz, deltaz+dz, dz):
                    if z <= chits[c.S_Z][hi] and chits[c.S_Z][hi] < z+dz: sz = z
            if sx is None or sy is None or sz is None:
                # NOTE: There is a very particular case where this conditional might be triggered
                #       "by accident". If either dx or dy perfectly divides 2*deltax or 2*deltay
                #       respectively and a hit happens exactly at an edge... kaboom, a hit is lost.
                #       The probability of this happening on a 64-bit computer is pretty low, so I
                #       don't think adding the extra computing time and error checking is worth it.
                print("ERROR: Either something is deeply wrong in the input data, or nrows and/or" \
                      " ncols is set wrong. It's probably the latter.", file=sys.stderr)
                exit()

            ok = str(int((deltax+sx)/dx)) + ',' + str(int((deltay+sy)/dy))
            if not math.isnan(dz):
                ok += ',' + str(int((deltaz+sz)/dz))
                if ok in phits: phits[ok].append((chits[c.S_PID][hi], chits[c.S_ED][hi]))
                else:           phits[ok] = [(chits[c.S_PID][hi], chits[c.S_ED][hi])]
            else:
                if ok not in phits:
                    phits[ok] = {c.S_GRUIDNHITS: 0, c.S_GRUIDEDEP: 0.}
                phits[ok][c.S_GRUIDNHITS] += 1
                phits[ok][c.S_GRUIDEDEP]  += chits[c.S_ED][hi]

            for ikey in chits.keys(): chits[ikey].pop(hi)
            hitstored = True

        if hitstored: tseries[t] = phits
    return tseries

def _gen_pd(hits, dt, vx, vy, vz, nx, ny, nz):
    """
    Generate list of massive particles passing through a plane.
    :param hits: list of hits in the output format of the extract_hits() method.
    :param vx:   x position for the vertex of the detecting plane.
    :param vy:   y position for the vertex of the detecting plane.
    :param vz:   z position for the vertex of the detecting plane.
    :param nx:   x direction for the vector of the detecting plane.
    :param ny:   y direction for the vector of the detecting plane.
    :param nz:   z direction for the vector of the detecting plane.
    """
    if not hits: return None
    chits = copy.deepcopy(hits) # Deep copy hits to avoid damaging original dictionary.

    # Prepare time series.
    tseries = {}
    max_t = 0.
    for t in chits[c.S_T]:
        if t > max_t: max_t = t
    for t in numpy.arange(0., max_t, dt):
        tseries[t] = {c.S_TID:[], c.S_TRKE:[], c.S_T:[], c.S_PID:[]}

    # Separate hits by TID.
    nhits = {}
    for hi in range(len(chits[c.S_N])-1, -1, -1):
        if chits[c.S_TID][hi] not in nhits.keys():
            nhits[chits[c.S_TID][hi]] = []
        nhits[chits[c.S_TID][hi]].append({
                c.S_X: chits[c.S_X][hi], c.S_Y:  chits[c.S_Y][hi],  c.S_Z:    chits[c.S_Z][hi],
                c.S_T: chits[c.S_T][hi], c.S_ED: chits[c.S_ED][hi], c.S_TRKE: chits[c.S_TRKE][hi],
                c.S_PID: chits[c.S_PID][hi]
        })

    # Order hits by time
    nhits2 = {}
    for k in nhits.keys():
        nhits2[k] = sorted(nhits[k], key=itemgetter(c.S_T))

    # Normalize the detecting plane's vector direction just in case.
    n = nx**2 + ny**2 + nz**2
    if n == 0:
        print("ERROR: normal vector is 0! Exiting...", file=sys.stderr)
        exit()
    if 0.99 > n or n > 1.01:
        nx /= n
        ny /= n
        nz /= n

    # Select tracks crossing through the plane.
    for trkid in nhits2.keys(): # Loop through tracks.
        for i in range(len(nhits2[trkid]) - 1): # Loop through hits.
            h0 = nhits2[trkid][i]
            h1 = nhits2[trkid][i+1]

            pdis  = nx*(vx-h0[c.S_X]) + ny*(vy-h0[c.S_Y]) + nz*(vz-h0[c.S_Z])
            alpha = nx*(h1[c.S_X]-h0[c.S_X]) + ny*(h1[c.S_Y]-h0[c.S_Y]) + nz*(h1[c.S_Z]-h0[c.S_Z])

            if -0.001 < alpha and alpha < 0.001 and -0.001 < pdis and pdis < 0.001:
                # Line lies on plane
                _add_trk(tseries, max_t, dt, trkid, h0[c.S_TRKE], h0[c.S_T], h0[c.S_PID])
            else:
                # Line intersects plane.
                rho = abs(pdis/alpha)
                if 0 <= rho and rho <= 1:
                    _add_trk(tseries, max_t, dt, trkid, h0[c.S_TRKE],
                             (1-rho)*h0[c.S_T] + rho*h1[c.S_T], h0[c.S_PID])

    # Remove empty entries from time series.
    for t in numpy.arange(0., max_t, dt):
        if not tseries[t][c.S_TID]: del tseries[t]

    return tseries

def _add_trk(trklist, max_t, dt, htid, hE, ht, hpid):
    """Find correct spot for track and add it to dictionary.
    """
    for t in numpy.arange(0., max_t, dt):
        if t < ht and ht < t+dt:
            trklist[t][c.S_TID] .append(htid)
            trklist[t][c.S_TRKE].append(hE)
            trklist[t][c.S_T]   .append(ht)
            trklist[t][c.S_PID] .append(hpid)

def generate_event(hits, in_nrows, in_ncols, dt, dx, dy, dz, pvx, pvy, pvz, pnx, pny, pnz):
    """
    Generates an event in a standard gruid .json format, as is described in the attached README.md.
    :param hits:  list of hits in the output format of the extract_hits() method.
    :param nrows: number of rows in the array of scintillating fibers.
    :param ncols: number of columns in the array of scintillating fibers.
    :param dt:    delta t for the time series in ns.
    :param dx:    size of the time series' matrix' columns in cm.
    :param dy:    size of the time series' matrix' rows in cm.
    :param dz:    size of the detector's body time series' matrix' depth columns in cm. If this is
                  NaN, we don't capture depth data at all.
    :param pvx:   x position for the vertex of the detecting plane. If this is NaN, the virtual
                  plane isn't used.
    :param pvy:   y position for the vertex of the detecting plane.
    :param pvz:   z position for the vertex of the detecting plane.
    :param pnx:   x direction for the vector of the detecting plane.
    :param pny:   y direction for the vector of the detecting plane.
    :param pnz:   z direction for the vector of the detecting plane.
    :return:      an array of 2-dimensional sparse matrix as per scipy sparce's csr_matrix
                  definition. To further reduce storage use, if not hits are found for a dt, a
                  NoneType object is stored instead of an empty matrix.
    """
    out_ncols  = math.ceil(2*c.DX(in_ncols)/dx)
    out_nrows  = math.ceil(2*c.DY(in_nrows)/dy)
    sarr       = [(c.S_GRUIDH1,c.S_PHOTONH1), (c.S_GRUIDH2,c.S_PHOTONH2)]
    event = {c.S_GRUIDMETA: {c.S_PID:hits[c.S_MASSHITS][c.S_PID][0],
             c.S_DT:dt, c.S_DX:dx, c.S_DY:dy, c.S_NROWS:out_nrows, c.S_NCOLS:out_ncols}}

    # Add detector depth data if needed.
    if not math.isnan(dz):
        sarr.append((c.S_GRUIDHB,c.S_MASSHITS))
        event[c.S_GRUIDMETA][c.S_DZ]     = dz
        event[c.S_GRUIDMETA][c.S_NDCOLS] = math.ceil(2*c.DZ/dz)

    # Obtain time series.
    for s in sarr:
        event[s[0]] = _gen_ts(hits[s[1]], c.DX(in_ncols), c.DY(in_nrows), c.DZ,
                              dt, dx, dy, dz if s[0]==c.S_GRUIDHB else float("nan"))

    # Obtain detecting plane data if needed.
    if not math.isnan(pvx):
        chits = {}
        for key in hits[c.S_MASSHITS]:
            chits[key] = hits[c.S_MASSHITS][key] + hits[c.S_PHOTONHITS][key]
        event[c.S_DPLANE] = _gen_pd(chits, dt, pvx, pvy, pvz, pnx, pny, pnz)
    return event
