# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles time series. Currently only generates a matrix time series for a set of GEMC hits.
"""

import copy
import math
import numpy as np
from scipy.sparse import csr_matrix

def generate_timeseries(hits, deltax, deltay, dt, dx, dy):
    """
    Generates a time series of sparse 2-dimensional matrices from a list of hits.
    :param hits:   list of hits in the output format of the extract_hits() method.
    :param deltax: how much the entire detector is shifted from the x axis. Used to obtain the size
                   of the generated matrices.
    :param deltay: how much the entire detector is shifted from the y axis. Used to obtain the size
                   of the generated matrices.
    :param dt:     delta t of the time series.
    :param dx:     size of the matrices' columns. Doesn't need to divide the total x size of the
                   detector.
    :param dy:     size of the matrices' rows. Doesn't need to divide the total y size of the
                   detector.
    :return:       an array of 2-dimensional sparse matrix as per scipy sparce's csr_matrix
                   definition. To further reduce storage use, if not hits are found for a dt, a
                   NoneType object is stored instead of an empty matrix.
    """
    if not hits: return None
    chits = copy.deepcopy(hits) # Deep copy hits to avoid damaging original array. Maybe overkill.

    tseries = []
    max_t = 0.
    for t in chits['t']:
        if t > max_t: max_t = t

    for t in np.arange(0., max_t, dt):
        hitstored = False
        m = np.zeros((int(math.ceil(2*deltay/dy)), int(math.ceil(2*deltax/dx))))

        for hi in range(len(chits['n'])-1, -1, -1):
            # Check if hit is in dt.
            if t > chits['t'][hi] or t+dt <= chits['t'][hi]: continue

            # Store hit's position.
            sx = None
            for x in np.arange(-deltax, deltax+dx, dx):
                if x <= chits['x'][hi] and chits['x'][hi] < x+dx: sx = x
            sy = None
            for y in np.arange(-deltay, deltay+dy, dy):
                if y <= chits['y'][hi] and chits['y'][hi] < y+dy: sy = y
            if not sx or not sy:
                # NOTE: There is a very particular case where this conditional might be triggered
                #       "by accident". If either dx or dy perfectly divides 2*deltax or 2*deltay
                #       respectively and a hit happens exactly at an edge... kaboom, a hit is lost.
                #       The probability of this happening in a 64-bit computer is pretty low, so I
                #       don't think adding the extra computing time and error checking is worth it.
                print("FATAL ERROR: Something is deeply wrong in the input data.", file=sys.stderr)
                exit()

            m[int((deltay+sy)/dy)][int((deltax+sx)/dx)] += chits['E'][hi]

            for key in chits.keys():
                chits[key].pop(hi)
            hitstored = True

        if not hitstored: tseries.append(None)
        else:             tseries.append(csr_matrix(m))
    return tseries
