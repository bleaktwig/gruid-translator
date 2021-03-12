#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
TODO.
"""

import file_io as io
import gemcevent_handler as gemc_eh
import gruidevent_handler as gruid_eh

# FLAGS
# --ifile (-i):   Input file to open. No default value.
# --fevent (-f):  First event to read. Useful when handling very large files. Note that events are
#                 counted from 1. Default is 1.
# --nevents (-n): Number of events to read, counting from the file set with --fevent. Set to 0 to
#                 read until the end of file. Default 0.
# --dt (-t):      No default value, must be set.
# --dx (-x):      No default value, must be set.
# --dy (-y):      No default value, must be set.
# --nrows (-r):   Number of rows used in the simulation. By default it's read from the filename. If
#                 unavailable, will be requested from the user.
# --ncols (-c):   Number of columns used in the simulation. By default it's read from the filename.
#                 if unavailable, will be requested from the user.
# --outamnt (-o): Amount of export files to be generated. Can be 0, 1, or 2. Default is 1.
#                   * 0: No files are exported, generated matrices are printed to std output.
#                   * 1: An output file containing the time series is generated in out/.
#                   * 2: Apart from the normal output file, two additional files are generated.
#                        "meta_$FILENAME.txt" contains the simulation metadata, and
#                        "hits_$FILENAME.txt" contains a list of hits per event as defined by gemc.

# What is set by flags:
ifile   = "/home/twig/data/code/babycal/bcal_generator/bcal_20210311122138_r11c11.txt"
fevent  = 1
nevents = 1
dt      = 0.05 # ns
dx      = 0.1  # cm
dy      = 0.1  # cm
nrows   = None
ncols   = None
outamnt = 0
# NOTE: Energy is in eV

(path, filename) = io.split_address(ifile)
if nrows is None and ncols is None: (nrows, ncols) = io.decode_filename(filename)
(metadata, events) = io.load_file(ifile, fevent, nevents)

ei = fevent
hitsdict  = {}
eventdict = {}
for event in events:
    key = filename + " event " + str(ei)
    hitsdict [key] = gemc_eh.extract_hits(event)
    eventdict[key] = gruid_eh.generate_event(hitsdict[key], nrows, ncols, dt, dx, dy)
    ei += 1
io.generate_output(eventdict, hitsdict, metadata, filename, outamnt)
