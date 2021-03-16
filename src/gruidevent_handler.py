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

import constants as c

def _gen_ts(hits, deltax, deltay, dt, dx, dy):
    """
    Generates a time series of sparse 2-dimensional matrices from a list of hits.
    :param hits:   list of hits in the output format of the extract_hits() method.
    :param deltax: how much the entire detector is shifted from the x axis. Used to obtain the size
                   of the generated matrices.
    :param deltay: how much the entire detector is shifted from the y axis. Used to obtain the size
                   of the generated matrices.
    :param dt:     delta t for the time series.
    :param dx:     size of the matrices' columns. Doesn't need to divide the total x size of the
                   detector.
    :param dy:     size of the matrices' rows. Doesn't need to divide the total y size of the
                   detector.
    :return:       a dictionary of 2-dimensional sparse matrices. Each matrix is defined as a
                   dictionary where a key is a tuple describing position and a value is the energy
                   deposited in eV. To further reduce storage use, if not hits are found for a
                   specific t, that t isn't event stored in the time series.
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
            if sx is None or sy is None:
                # NOTE: There is a very particular case where this conditional might be triggered
                #       "by accident". If either dx or dy perfectly divides 2*deltax or 2*deltay
                #       respectively and a hit happens exactly at an edge... kaboom, a hit is lost.
                #       The probability of this happening on a 64-bit computer is pretty low, so I
                #       don't think adding the extra computing time and error checking is worth it.
                print("ERROR: Either something is deeply wrong in the input data, or nrows and/or " \
                      "ncols is set wrong. It's probably the latter.", file=sys.stderr)
                exit()

            key = str(int((deltay+sy)/dy)) + "," + str(int((deltax+sx)/dx))
            if key in phits: phits[key] += chits[c.S_E][hi]
            else:            phits[key]  = chits[c.S_E][hi]

            for key in chits.keys(): chits[key].pop(hi)
            hitstored = True

        if hitstored: tseries[t] = phits
    return tseries

def generate_event(hits, in_nrows, in_ncols, dt, dx, dy):
    """
    Generates an event in a standard gruid .json format, as is described in the attached README.md.
    :param hits:  list of hits in the output format of the extract_hits() method.
    :param nrows: number of rows in the array of scintillating fibers.
    :param ncols: number of columns in the array of scintillating fibers.
    :param dt:    delta t for the time series in ns.
    :param dx:    size of the time series' matrix' columns in cm.
    :param dy:    size of the time series' matrix' rows in cm.
    :return:      an array of 2-dimensional sparse matrix as per scipy sparce's csr_matrix
                  definition. To further reduce storage use, if not hits are found for a dt, a
                  NoneType object is stored instead of an empty matrix.
    """
    out_nrows = math.ceil(2*c.DELTAY(in_nrows)/dy)
    out_ncols = math.ceil(2*c.DELTAX(in_ncols)/dx)
    event = {c.S_GRUIDMETA: {c.S_DT:dt, c.S_DX:dx, c.S_DY:dy, c.S_NROWS:out_nrows, c.S_NCOLS:out_ncols}}
    event[c.S_GRUIDH1] = _gen_ts(hits[c.S_PHOTONH1], c.DELTAX(in_ncols), c.DELTAY(in_nrows), dt, dx, dy)
    event[c.S_GRUIDH2] = _gen_ts(hits[c.S_PHOTONH2], c.DELTAX(in_ncols), c.DELTAY(in_nrows), dt, dx, dy)
    return event
