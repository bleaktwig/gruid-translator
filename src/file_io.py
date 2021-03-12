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

def generate_outfilename(addr, ed):
    """generate the output filename.
    """
    f = None
    l = None
    for key in ed.keys():
        n = int(key.split(' ')[-1])
        if f is None: f = n
        if l is None: l = n
        if n < f: f = n
        if l < n: l = n
    return '_'.join('.'.join(addr.split('.')[0:-1]).split('_')[0:-1])+"_"+str(f)+"-"+str(l)+".json"

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

        ei = 0
        while True:
            event = fh.store_event(f)
            if not event: break # Reached end of file.
            ei += 1
            if ei < fevent: continue # Dump events before first to be read.
            events.append(event)
            if nevents != 0 and ei-fevent+1 >= nevents: break

    return (metadata, events)

def generate_output(eventdict, hitsdict, metadata, filename, outamnt=0):
    """Calls appropiate output function based in outamnt.
    """
    switch = [_export0, _export1, _export2]
    switch[outamnt](eventdict, hitsdict, metadata, filename)

def _export0(eventdict, hitsdict, metadata, in_filename):
    print(json.dumps(eventdict, indent=4, sort_keys=True))

def _export1(eventdict, hitsdict, metadata, in_filename):
    Path(c.OUTPATH).mkdir(exist_ok=True)
    with open(c.OUTPATH + "/out_" + generate_outfilename(in_filename, eventdict), 'w') as f:
        json.dump(eventdict, f, indent=4, sort_keys=True)

def _export2(eventdict, hitsdict, metadata, in_filename):
    print("TODO2")
    # Path(c.OUTPATH).mkdir(exist_ok=True)
    # eventdict["gemc metadata"] = metadata
    #
    # print(hitsdict['bcal_20210311122138_r11c11.txt event 1'][0]['E'])
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # return
