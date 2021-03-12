# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles GEMC events. Currently only extracts the relevant hits for an event.
"""

import constants as c

def extract_hits(event):
    """
    Extract hits from an event.
    :param event: one event in the format defined by the store_event() method.
    :return:      a 2-tuple containing dictionaries describing the hits in arrays. Dictionaries'
                  keys are the following:
                    * n: hit identifier. Unused by this program, but useful in reconstruction.
                    * x: x position of the hit in cm.
                    * y: y position of the hit in cm.
                    * t: time of the hit in ns (t=0 is defined as the moment when the event takes
                         place).
                    * E: energy deposited by the hit in eV.
    """
    if event is None: return None
    # Define hits dictionaries (one per detecting surface).
    hits = {c.S_GEMCH1: {c.S_N : [], c.S_X : [], c.S_Y : [], c.S_T : [], c.S_E : [],},
            c.S_GEMCH2: {c.S_N : [], c.S_X : [], c.S_Y : [], c.S_T : [], c.S_E : [],},}

    for hi in range(len(event[c.IDBANK][c.S_HITN])):
        if event[c.IRBANK][c.S_PID] [hi] != '0': continue # Ignore hits not from photons.
        if event[c.IRBANK][c.S_EDEP][hi] == '0': continue # Ignore hits with no energy deposited.
        vol = None # Save the volume hit.
        volid = int(int(event[c.IDBANK][c.S_VOL][hi])/10**8)
        if volid == c.SENSOR1A_ID or volid == c.SENSOR1B_ID: vol = c.S_GEMCH1
        if volid == c.SENSOR2A_ID or volid == c.SENSOR2B_ID: vol = c.S_GEMCH2
        if vol is None: continue

        # Add hit to dictionary, converting them to their appropiate units.
        hits[vol][c.S_N].append(float(event[c.IDBANK][c.S_HITN][hi]))       # hit identifier.
        hits[vol][c.S_X].append(float(event[c.IRBANK][c.S_AVGX][hi])/10.)   # x position (in cm).
        hits[vol][c.S_Y].append(float(event[c.IRBANK][c.S_AVGY][hi])/10.)   # y position (in cm).
        hits[vol][c.S_T].append(float(event[c.IRBANK][c.S_AVGT][hi]))       # Time (in ns).
        hits[vol][c.S_E].append(float(event[c.IRBANK][c.S_EDEP][hi])*10**6) # Energy deposited (in eV).

    return hits
