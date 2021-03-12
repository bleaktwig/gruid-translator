# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles interactions with GEMC the file, as in storing metadata and events. Is not allowed direct
access to IO.
"""

import constants as c

def store_metadata(file):
    """
    Store file's metadata as a dictionary of strings.
    :param file: unprocessed input file.
    :return:     dictionary of metadata.
    """
    metadata = {}
    filetype = False # Check if the file has an embedded json.

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
    Store one event's data as a dictionary of dictionaries, assuming that the metadata has already
    been stored.
    :param file: input file with metadata (and pesky embedded json) removed.
    :return:     a dict with 5 dicts whose keys are the 5 BANK constants. Each describes the
                 following:
                   * HBANK:  header bank (10).
                   * UHBANK: user header bank (currently empty). Assumed to have same format as
                             header bank.
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
