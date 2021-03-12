# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles files, as in loading GEMC files and saving sparse matrices as external output files. Is the
only file allowed to handle IO.
"""

import json
import re
import gemcfile_handler as fh

def split_address(addr):
    """Split an address into path and filename.
    """
    addrlist = addr.split('/')
    return ('/'.join(addrlist[0:-1]), addrlist[-1])

def decode_filename(addr):
    """Decode filename and return nrows and ncols in one line.
    """
    return [int(re.findall(r'\d+', addr)[i]) for i in range(-2, 0)]

def load_file(addr, fevent=0, nevents=0):
    """
    Store a GEMC file's metadata and events in a tuple.
    :param addr:    address of the input file in standard GEMC txt format.
    :param fevent:  first event to read. Useful when handling very large files.
    :param nevents: number of events to read. Set to 0 to read all events.
    :return:        a 2-tuple with a dictionary containing the file's metadata (0) and an array of
                    events (1). Both the metadata's and each event's formats are described in the
                    store_metadata() and store_event() methods.
    """
    f = open(addr)

    metadata = fh.store_metadata(f)
    events  = []

    nevent = 0
    while True:
        nevent += 1
        if nevent <= fevent: continue
        event = fh.store_event(f)
        if not event: break # Reached end of file.
        events.append(event)
        if nevents != 0 and nevent >= nevents: break
    f.close()

    return (metadata, events)

def generate_output(eventdict, path, filename, outamnt=0):
    """Calls appropiate output function based in outamnt.
    """
    switch = [_export0, _export1, _export2]
    switch[outamnt](eventdict, path, filename)

def _export0(eventdict, path, in_filename):
    print(json.dumps(eventdict, indent=4, sort_keys=True))

def _export1(eventdict, path, in_filename):
    out_filename = '/'.join(path.split('/')[0:-1]) + "/out/"
    with open("../out/result.json", 'w') as fp:
        json.dump(eventdict, fp, indent=4, sort_keys=True)

def _export2(eventdict, path, in_filename):
    print("TODO 2")
