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
# --fevent (-f):  First event to read. Useful when handling very large files. Default is 0.
# --nevents (-n): Number of events to read, counting from the file set with --fevent. Set to 0 to
#                 read until the end of file. Default 0.
# --dt (-t):      No default value, must be set.
# --dx (-x):      No default value, must be set.
# --dy (-y):      No default value, must be set.
# --nrows (-r):   Number of rows used in the simulation. By default it's read from the filename. If
#                 unavailable, will be requested from the user.
# --ncols (-c):   Number of columns used in the simulation. By default it's read from the filename.
#                 if unavailable, will be requested from the user.
# --outamnt (-o):  Amount of export files to be generated. Can be 0, 1, or 2. Default is 1.
#                   * 0: No files are exported, generated matrices are printed to std output.
#                   * 1: An output file containing the time series is generated.
#                   * 2: Apart from the normal output file, two additional files are generated.
#                        "meta_$FILENAME.txt" contains the simulation metadata, and
#                        "hits_$FILENAME.txt" contains a list of hits per event.

# What is set by flags:
ifile   = "/home/twig/data/code/babycal/bcal_generator/bcal_20210311122138_r11c11.txt"
fevent  = 0
nevents = 5
dt      = 0.05 # ns
dx      = 0.1  # cm
dy      = 0.1  # cm
nrows   = 0
ncols   = 0
# NOTE: Energy is in eV

# TO BE HANDLED
outamnt = 0

if nrows == 0 and ncols == 0: (nrows, ncols) = io.decode_filename(ifile)
(metadata, events) = io.load_file(ifile, fevent, nevents)
ei = fevent
eventdict = {}
for event in events:
    ei += 1
    hits = gemc_eh.extract_hits(event)
    eventdict[ei] = gruid_eh.generate_event(ei, hits, nrows, ncols, dt, dx, dy)
io.generate_output(eventdict, outamnt)
