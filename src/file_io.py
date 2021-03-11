# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles files, as in loading GEMC files and saving sparse matrices as external output files. Is the
only file allowed to handle IO.
"""

import file_handler as f_handler

def load_file(addr, nevents=0):
    """
    Store a GEMC file's metadata and events in a tuple.
    :param addr:    address of the input file in standard GEMC txt format.
    :param nevents: number of events to read. Set to 0 to read all events.
    :return:        a 2-tuple with a dictionary containing the file's metadata (0) and an array of
                    events (1). Both the metadata's and each event's formats are described in the
                    store_metadata() and store_event() methods.
    """
    f = open(addr)

    metadata = f_handler.store_metadata(f)
    events  = []

    nevent = 0
    while True:
        nevent += 1
        event = f_handler.store_event(f)
        if not event: break # Reached end of file.
        events.append(event)
        if nevents != 0 and nevent >= nevents: break
    f.close()

    return (metadata, events)
