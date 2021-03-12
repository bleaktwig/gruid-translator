# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles gruid events. Generates gruid events with matrix time series for a set of GEMC hits.
"""

import copy
import math
import numpy # TODO: We could do without numpy...

import constants as c

def generate_timeseries(hits, deltax, deltay, dt, dx, dy):
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
                   deposited in eV. To further reduce storage use, if not hits are found for a dt, a
                   NoneType object is stored instead of an empty matrix.
    """
    if not hits: return None
    chits = copy.deepcopy(hits) # Deep copy hits to avoid damaging original array.

    tseries = {}
    max_t = 0.
    for t in chits['t']:
        if t > max_t: max_t = t

    for t in numpy.arange(0., max_t, dt):
        hitstored = False
        phits = {}

        for hi in range(len(chits['n'])-1, -1, -1):
            # Check if hit is in dt.
            if t > chits['t'][hi] or t+dt <= chits['t'][hi]: continue

            # Store hit's position.
            sx = None
            for x in numpy.arange(-deltax, deltax+dx, dx):
                if x <= chits['x'][hi] and chits['x'][hi] < x+dx: sx = x
            sy = None
            for y in numpy.arange(-deltay, deltay+dy, dy):
                if y <= chits['y'][hi] and chits['y'][hi] < y+dy: sy = y
            if not sx or not sy:
                # NOTE: There is a very particular case where this conditional might be triggered
                #       "by accident". If either dx or dy perfectly divides 2*deltax or 2*deltay
                #       respectively and a hit happens exactly at an edge... kaboom, a hit is lost.
                #       The probability of this happening in a 64-bit computer is pretty low, so I
                #       don't think adding the extra computing time and error checking is worth it.
                print("FATAL ERROR: Something is deeply wrong in the input data.", file=sys.stderr)
                exit()
            phits[(int((deltay+sy)/dy),int((deltax+sx)/dx))] = chits['E'][hi]*10**6

            for key in chits.keys():
                chits[key].pop(hi)
            hitstored = True

        if not hitstored: tseries[t] = None
        else:             tseries[t] = phits
    return tseries

def generate_event(ei, hits, nrows, ncols, dt, dx, dy):
    """
    Generates an event in a standard gruid .json format, as is described in the attached README.md.
    :param ei:    event number.
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
    event = {"metadata": {"dt":dt, "dx":dx, "dy":dy, "nrows":nrows, "ncols":ncols}}
    for i in range(2):
        event["side " + str(i+1)] = \
                generate_timeseries(hits[i], c.DELTAX(ncols), c.DELTAY(nrows), dt, dx, dy)
    return event
