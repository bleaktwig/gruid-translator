#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
TODO.
"""

import math
import copy
import numpy as np
from scipy.sparse import csr_matrix

import constants as c
import file_io as io

# FLAGS
# --filename or -f: Filename to open. No default value.
# --nevents or -n: Default 0.
# --dt: no default value, must be set.
# --dx: no default value, must be set.
# --dy: no default value, must be set.

# Define these based on the input file (TODO: Should be written into the file).
NROWS = 11
NCOLS = 11

(metadata, events) = io.load_file("/home/twig/data/code/babycal/bcal_generator/output_test_1.txt")

import pprint
pp = pprint.PrettyPrinter(indent=4, width=100, compact=True)

pp.pprint(metadata)

# Extract hits from an event.
def extract_hits(event):
    """
    Extract hits from an event.
    :param event: one event in the format defined by the store_event() method.
    :return:      a 2-tuple containing dictionaries describing the hits in arrays. Dictionaries' keys are the
                  following:
                    * n: hit identifier. Unused by this program, but useful in reconstruction.
                    * x: x position of the hit in cm.
                    * y: y position of the hit in cm.
                    * t: time of the hit in ns (t=0 is defined as the moment when the event takes place).
                    * E: energy deposited by the hit.
    """
    if event == None: return None
    # Define hits dictionaries (one per detecting surface).
    hits = ({'n' : [], 'x' : [], 'y' : [], 't' : [], 'E' : [],},
            {'n' : [], 'x' : [], 'y' : [], 't' : [], 'E' : [],},)

    for hi in range(len(event[c.IDBANK][c.S_HITN])):
        if event[c.IRBANK]["pid"]    [hi] != '0': continue # Ignore hits that don't come from photons.
        if event[c.IRBANK]["totEdep"][hi] == '0': continue # Ignore hits with no energy deposited.
        vol = -1 # Save the volume hit.
        volid = int(int(event[c.IDBANK][c.S_VOL][hi])/10**8)
        if volid == c.SENSOR1A_ID or volid == c.SENSOR1B_ID: vol = 0
        if volid == c.SENSOR2A_ID or volid == c.SENSOR2B_ID: vol = 1
        if vol == -1: continue

        # Add hit to dictionary.
        hits[vol]['n'].append(float(event[c.IDBANK][c.S_HITN][hi]))  # hit identifier.
        hits[vol]['x'].append(float(event[c.IRBANK][c.S_X][hi])/10.) # x position (in cm).
        hits[vol]['y'].append(float(event[c.IRBANK][c.S_Y][hi])/10.) # y position (in cm).
        hits[vol]['t'].append(float(event[c.IRBANK][c.S_T][hi]))     # Time.
        hits[vol]['E'].append(float(event[c.IRBANK][c.S_E][hi]))     # Energy deposited.

    return hits

def generate_timeseries(hits, dt, dx, dy):
    """
    Generates a time series of sparse 2-dimensional matrices from a list of hits.
    :param hits: list of hits in the output format of the extract_hits() method.
    :param dt:   delta t of the time series.
    :param dx:   size of the matrix's columns. Doesn't need to divide the total x size of the detector.
    :param dy:   size of the matrix's rows. Doesn't need to divide the total y size of the detector.
    :return:     an array of 2-dimensional sparse matrix as per scipy sparce's csr_matrix definition. To further
                 reduce storage use, if not hits are found for a dt a null object is stored instead of an empty
                 matrix.
    """
    if not hits: return None
    chits = copy.deepcopy(hits) # NOTE: Maybe overkill.

    tseries = []
    max_t = 0.
    for t in chits['t']:
        if t > max_t: max_t = t

    for t in np.arange(0., max_t, dt):
        hitstored = False
        m = np.zeros((int(math.ceil(2*c.DELTAY(NROWS)/dy)), int(math.ceil(2*c.DELTAX(NCOLS)/dx))))

        for hi in range(len(chits['n'])-1, -1, -1):
            # Check if hit is in dt.
            if t > chits['t'][hi] or t+dt <= chits['t'][hi]: continue

            # Store hit's position.
            sx = None
            for x in np.arange(-c.DELTAX(NCOLS), c.DELTAX(NCOLS)+dx, dx):
                if x <= chits['x'][hi] and chits['x'][hi] < x+dx: sx = x
            sy = None
            for y in np.arange(-c.DELTAY(NROWS), c.DELTAY(NROWS)+dy, dy):
                if y <= chits['y'][hi] and chits['y'][hi] < y+dy: sy = y
            if not sx or not sy:
                # NOTE: There is a very particular case where this conditional might be triggered "by accident". If either dx or dy
                #       perfectly divides 2*DELTAX or 2*DELTAY respectively, and a hit happens exactly at an
                #       edge... kaboom. The probability of this happening in a 64-bit computer is so low that I don't think adding the
                #       extra computing time and error checking is worth it.
                print("Something is deeply wrong in the input data. Exiting...")
                return None

            m[int((c.DELTAY(NROWS)+sy)/dy)][int((c.DELTAX(NCOLS)+sx)/dx)] += chits['E'][hi]

            for key in chits.keys():
                chits[key].pop(hi)
            hitstored = True

        if not hitstored: tseries.append(None)
        else:             tseries.append(csr_matrix(m))
    return tseries
