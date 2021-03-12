# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Handles files, as in loading GEMC files and saving sparse matrices as external output files. Is the
only file allowed to handle IO.
"""

from pathlib import Path
import json
import re
import constants as c
import gemcfile_handler as fh

outpath = "../out"

def split_address(addr):
    """Split an address into path and filename.
    """
    addrlist = addr.split('/')
    return ('/'.join(addrlist[0:-1]), addrlist[-1])

def decode_filename(addr):
    """Decode filename and return nrows and ncols in one line.
    """
    return [int(re.findall(r'\d+', addr)[i]) for i in range(-2, 0)]

def generate_outfilename(addr, f, n):
    """generate the output filename.
    """
    return '_'.join('.'.join(addr.split('.')[0:-1]).split('_')[0:-1])+"_"+str(f)+"-"+str(f+n-1)+".json"

def load_file(addr, fevent=1, nevents=0):
    """
    Store a GEMC file's metadata and events in a tuple.
    :param addr:    address of the input file in standard GEMC txt format.
    :param fevent:  first event to read. Useful when handling very large files.
    :param nevents: number of events to read. Set to 0 to read all events from fevent onward.
    :return:        a 2-tuple with a dictionary containing the file's metadata (0) and an array of
                    events (1). Both the metadata's and each event's formats are described in the
                    store_metadata() and store_event() methods.
    """
    with open(addr) as f:
        metadata = fh.store_metadata(f)
        events  = []

        nevent = fevent
        while True:
            event = fh.store_event(f)
            if not event: break # Reached end of file.
            events.append(event)
            if nevents != 0 and nevent-fevent >= nevents: break
            nevent += 1

    return (metadata, events)

def generate_output(eventdict, filename, fevent, nevents, outamnt=0):
    """Calls appropiate output function based in outamnt.
    """
    switch = [_export0, _export1, _export2]
    switch[outamnt](eventdict, filename, fevent, nevents)

def _export0(eventdict, in_filename, fevent, nevents):
    print(json.dumps(eventdict, indent=4, sort_keys=True))

def _export1(eventdict, in_filename, fevent, nevents):
    Path(c.OUTPATH).mkdir(exist_ok=True)
    with open(c.OUTPATH + "/" + generate_outfilename(in_filename, fevent, nevents), 'w') as f:
        json.dump(eventdict, f, indent=4, sort_keys=True)

def _export2(eventdict, in_filename, fevent, nevents):
    print("TODO 2")
