#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
TODO.
"""

import constants as c
import file_io as io
import event_handler as e_handler
import tseries_handler as ts_handler

# FLAGS
# --ifile or -i: Input file to open. No default value.
# --ofile or -o: Output file that contains the matrix time series to create. By default is out.txt
# --fevent or -f: First event to read. Useful when handling very large files. Default is 0.
# --nevents or -n: Number of events to read, counting from the file set with --fevent. Set to 0  Default 0.
# --dt: no default value, must be set.
# --dx: no default value, must be set.
# --dy: no default value, must be set.

# Define these based on the input file (TODO: Should be written into the file).
NROWS = 11
NCOLS = 11

dt = 0.05
dx = 0.1
dy = 0.1

import pprint
pp = pprint.PrettyPrinter(indent=4, width=100, compact=True)

(metadata, events) = io.load_file("/home/twig/data/code/babycal/bcal_generator/output_test_1.txt")
for event in events:
    hits = e_handler.extract_hits(event)
    tseries = [ts_handler.generate_timeseries(hits[i], c.DELTAX(NCOLS), c.DELTAY(NROWS), dt, dx, dy)
               for i in range(2)]
    pp.pprint(tseries)
