# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles GEMC events. Currently only extracts the relevant hits for an event.
"""

import copy
import constants as c

def extract_hits(event):
    """
    Extract photon and predefined massive particle hits with energy larger than 0 from an event.
    :param event: one event in the format defined by the store_event() method.
    :return:      A dictionary containing 3 dictionaries that describe the hits. The three
                  dictionaries contain the particle hits --which generate the photons--, and the
                  photon hits that deposited energy in the endplates. The first is added to the
                  output of the program, while the two other are used to generate the gruid hits.
                  The dictionaries' keys are the following:
                    * n: hit identifier. Unused by this program, but useful in reconstruction.
                    * x: x position of the hit in cm.
                    * y: y position of the hit in cm.
                    * t: time of the hit in ns (t=0 is defined as the moment when the event takes
                         place).
                    * Edep: energy deposited by the hit in eV.
                    * TrkE: energy of the track to which the hit belongs.
    """
    if event is None: return None
    # Define hits dictionaries (one per detecting surface).
    hitdict = {c.S_N:[], c.S_ID:[], c.S_PID:[], c.S_X:[], c.S_Y:[], c.S_Z:[], c.S_T:[],
               c.S_ED:[], c.S_TRKE:[]}
    pidlist = [c.S_MMPID, c.S_MPPID, c.S_EMPID, c.S_EPPID, c.S_NPID]
    hits = {c.S_MASSHITS:   copy.deepcopy(hitdict),
            c.S_PHOTONHITS: copy.deepcopy(hitdict),
            c.S_PHOTONH1:   copy.deepcopy(hitdict),
            c.S_PHOTONH2:   copy.deepcopy(hitdict),}

    for hi in range(len(event[c.IDBANK][c.S_HITN])):
        if event[c.IRBANK][c.S_EDEP][hi] == '0': continue # Ignore hits with no energy deposited.

        # Determine hit source.
        key = None
        if event[c.IRBANK][c.S_PID][hi] in pidlist:         key = c.S_MASSHITS
        elif event[c.IRBANK][c.S_PID][hi] == c.S_PHOTONPID: key = c.S_PHOTONHITS

        # Process photon hits
        if key == c.S_PHOTONHITS:
            volid = int(int(event[c.IDBANK][c.S_VOL][hi])/10**8)
            if volid == c.SENSOR1A_ID or volid == c.SENSOR1B_ID: key = c.S_PHOTONH1
            if volid == c.SENSOR2A_ID or volid == c.SENSOR2B_ID: key = c.S_PHOTONH2

        if key is None: continue # Ignore uninteresting hits.

        # Add hit to dictionary, converting data to appropiate units.
        hits[key][c.S_N]   .append(int  (event[c.IDBANK][c.S_HITN]  [hi]))     # hit id.
        hits[key][c.S_ID]  .append(int  (event[c.IRBANK][c.S_TID]   [hi]))     # track id.
        hits[key][c.S_PID] .append(int  (event[c.IRBANK][c.S_PID]   [hi]))     # particle id.
        hits[key][c.S_X]   .append(float(event[c.IRBANK][c.S_AVGX]  [hi])/10.) # x position (cm).
        hits[key][c.S_Y]   .append(float(event[c.IRBANK][c.S_AVGY]  [hi])/10.) # y position (cm).
        hits[key][c.S_Z]   .append(float(event[c.IRBANK][c.S_AVGZ]  [hi])/10.) # z position (cm).
        hits[key][c.S_T]   .append(float(event[c.IRBANK][c.S_AVGT]  [hi]))     # Time (ns).
        hits[key][c.S_ED]  .append(float(event[c.IRBANK][c.S_EDEP]  [hi]))     # EDep (MeV).
        hits[key][c.S_TRKE].append(float(event[c.IRBANK][c.S_TRACKE][hi]))     # TrkE (MeV).

    return hits
