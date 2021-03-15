#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
TODO.
"""

import argparse
import sys
import constants as c
import file_io as io
import gemcevent_handler as gemc_eh
import gruidevent_handler as gruid_eh

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",        help=c.IHELP)
    parser.add_argument("dt",              help=c.THELP, type=float)
    parser.add_argument("dx",              help=c.XHELP, type=float)
    parser.add_argument("dy",              help=c.YHELP, type=float)
    parser.add_argument("-f", "--fevent",  help=c.FHELP, type=int)
    parser.add_argument("-n", "--nevents", help=c.NHELP, type=int)
    parser.add_argument("-o", "--outtype", help=c.OHELP, type=int)
    parser.add_argument("-r", "--nrows",   help=c.RHELP, type=int)
    parser.add_argument("-c", "--ncols",   help=c.CHELP, type=int)
    args = parser.parse_args()
    return args

def run(ifile, dt, dx, dy, fevent, nevents, outtype, nrows, ncols):
    (path, filename) = io.split_address(ifile)
    if nrows is None and ncols is None: (nrows, ncols) = io.decode_filename(filename)
    (metadata, events) = io.load_file(ifile, fevent, nevents)

    ei = fevent
    gemchitsdict = {}
    gruidhitsdict   = {}
    for event in events:
        key = filename + " event " + str(ei)
        gemchitsdict[key]  = gemc_eh.extract_hits(event)
        gruidhitsdict[key] = gruid_eh.generate_event(gemchitsdict[key], nrows, ncols, dt, dx, dy)
        ei += 1
    io.generate_output(gruidhitsdict, gemchitsdict, metadata, filename, outtype)

def main():
    args = setup_parser()

    # Process arguments.
    ifile = args.filename
    dt = args.dt
    dx = args.dx
    dy = args.dy
    fevent = 1
    if args.fevent: fevent = args.fevent
    nevents = 0
    if args.nevents: nevents = args.nevents
    outtype = 2
    if args.outtype:
        outtype = args.outtype
        if outtype < 1 or outtype > 5:
            print("ERROR: OUTTYPE should be between 1 and 5. Exiting...", file=sys.stderr)
            exit()
    nrows = None
    if args.nrows: nrows = args.nrows
    ncols = None
    if args.ncols: ncols = args.ncols

    run(ifile, dt, dx, dy, fevent, nevents, outtype, nrows, ncols)

if __name__ == "__main__":
    main()
