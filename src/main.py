#!/usr/bin/env python3.9

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

# Define these based on the input file (TODO: Should be written into this file).
NROWS = 11
NCOLS = 11

def store_metadata(file):
    """
    Store file's metadata as a dictionary of strings.
    :param file: unprocessed input file.
    :return:     dictionary of metadata.
    """
    metadata = {}
    filetype = False # Recent files have an embedded json for some reason.

    for i in range(2):
        devnull = file.readline() # Ignore the first two lines.

    while True:
        x = file.tell() # Define a stopping point for later.
        l = file.readline()
        if len(l) <= 4:
            filetype = True
            break
        if l[3] != '>':
            break
        sl = l.split(' ')
        if len(sl) == 7:
            metadata[sl[5]] = sl[6][:-1]

    if filetype:
        while True:
            x = file.tell()
            l = file.readline()
            if len(l) <= 4: continue
            if l[1] == '-': break

    file.seek(x)
    return metadata

def store_event(file):
    """
    Store one event's data as a dictionary of dictionaries, assuming that the metadata has already been stored.
    :param file: input file with metadata (and pesky embedded json) removed.
    :return:     a dict with 5 dicts whose keys are the 5 BANK constants. Each describes the following:
                   * HBANK:  header bank (10).
                   * UHBANK: user header bank (currently empty). Assumed to have same format as header bank.
                   * IRBANK: integrated raw bank (51).
                   * IDBANK: integrated digitized bank (52).
                   * GPBANK: generated particles bank.
    """
    event_data = {
        c.HBANK  : {},
        c.UHBANK : {},
        c.IRBANK : {},
        c.IDBANK : {},
        c.GPBANK : {},
    }
    bank = None
    eof = 0 # End of file checker.

    while True:
        l = file.readline()
        l = l[:-1].rstrip()
        if l == c.S_EOE:
            break
        if l == '':
            eof = 1
            break

        # Make sure we're writing to the correct address.
        if   l == c.S_HBANK:  bank = c.HBANK
        elif l == c.S_UHBANK: bank = c.UHBANK
        elif l == c.S_IRBANK: bank = c.IRBANK
        elif l == c.S_IDBANK: bank = c.IDBANK
        elif l == c.S_GPBANK: bank = c.GPBANK

        if bank != c.GPBANK:
            sl = l.split('\t')
            if len(sl) == 1: continue # Ignore lines with titles & irrelevant information.

        if bank == c.HBANK or bank == c.UHBANK: # Header & user header banks.
            event_data[bank][sl[0].split(' ')[-1][:-1]] = sl[1]
        if bank == c.IRBANK or bank == c.IDBANK: # Raw & Digitized banks.
            event_data[bank][sl[0].split(' ')[-1][:-1]] = sl[1:]
        if bank == c.GPBANK: # Generated particles bank.
            sl = l.split()
            if sl[1] == c.S_PARTICLE:
                event_data[bank][sl[ 3][:-1]] = sl[ 4]
                event_data[bank][sl[ 6][:-1]] = sl[ 7]
                event_data[bank][sl[10][:-1]] = sl[11]
            if sl[1] == c.S_HIT:
                event_data[bank][c.S_NHITS] = sl[ 4]
                event_data[bank][sl[ 7]]  = sl[ 8]
                event_data[bank][sl[11]]  = sl[12]
    if eof != 0:
        return None

    return event_data

def save_file(addr, nevents=0):
    """
    Store a GEMC file's metadata and events in a tuple.
    :param addr:    address of the input file in standard GEMC txt format.
    :param nevents: number of events to read. Set to 0 to read all events.
    :return:        a 2-tuple with a dictionary containing the file's metadata (0) and an array of events (1).
                    Both the metadata's and each event's formats are described in the store_metadata() and
                    store_event() methods.
    """
    f = open(addr)

    metadata = store_metadata(f)
    events  = []

    nevent = 0
    while True:
        nevent += 1
        event = store_event(f)
        if not event: break # Reached end of file.
        events.append(event)
        if nevents != 0 and nevent >= nevents: break
    f.close()

    return (metadata, events)

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
