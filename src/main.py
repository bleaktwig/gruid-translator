#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
Gruid Translator is a small tool in Python that attempts to convert a GEMC simulation of a generic
calorimeter detector to a format more similar to how the output is seen in real life.

Taking a .txt file exported by bcal_generator (https://github.com/emolinac/bcal), this tool
generates a time series of sparse matrices detailing the location and energy deposited of hits in
the scintillating fibers. It can also export these matrices as .json files for easy loading.
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
    parser.add_argument("-z", "--dz",      help=c.ZHELP, type=float)
    parser.add_argument("--pvx",           help=c.PVXHELP, type=float)
    parser.add_argument("--pvy",           help=c.PVYHELP, type=float)
    parser.add_argument("--pvz",           help=c.PVZHELP, type=float)
    parser.add_argument("--pnx",           help=c.PNXHELP, type=float)
    parser.add_argument("--pny",           help=c.PNYHELP, type=float)
    parser.add_argument("--pnz",           help=c.PNZHELP, type=float)
    parser.add_argument("-f", "--fevent",  help=c.FHELP, type=int)
    parser.add_argument("-n", "--nevents", help=c.NHELP, type=int)
    parser.add_argument("-o", "--outtype", help=c.OHELP, type=int)
    parser.add_argument("-r", "--nrows",   help=c.RHELP, type=int)
    parser.add_argument("-c", "--ncols",   help=c.CHELP, type=int)
    args = parser.parse_args()
    return args

def run(ifile, dt, dx, dy, dz, pvx, pvy, pvz, pnx, pny, pnz, fevent, nevents, outtype, nrows, ncols):
    (path, filename) = io.split_address(ifile)
    if nrows is None and ncols is None: (nrows, ncols) = io.decode_filename(filename)
    (metadata, events) = io.load_file(ifile, fevent, nevents)

    ei  = fevent
    ged = {}
    grd = {}
    for event in events:
        key = filename + ' ' + c.S_EVENT + ' ' + str(ei)
        ei += 1
        ged[key] = gemc_eh.extract_hits(event)
        if len(ged[key][c.S_MASSHITS][c.S_N]) == 0 or \
                (len(ged[key][c.S_PHOTONH1][c.S_N])==0 and len(ged[key][c.S_PHOTONH2][c.S_N])==0):
            del ged[key]
            continue
        grd[key] = gruid_eh.generate_event(ged[key], nrows, ncols, dt, dx, dy, dz,
                                           pvx, pvy, pvz, pnx, pny, pnz)
    io.generate_output(grd, ged, metadata, filename, fevent, nevents, outtype)

def main():
    args = setup_parser()

    # Process arguments.
    ifile = args.filename
    # Time series args.
    dt = args.dt
    dx = args.dx
    dy = args.dy
    dz = float("nan")
    if args.dz: dz = args.dz

    # Detecting plane.
    plane_arr = [args.pvx, args.pvy, args.pvz, args.pnx, args.pny, args.pnz]
    if not all(arg is None for arg in plane_arr):
        if None in plane_arr:
            print("ERROR: If one detecting plane variable is specified all should be! Exiting...",
                    file=sys.stderr)
            exit()

    pvx = float("nan")
    pvy = float("nan")
    pvz = float("nan")
    pnx = float("nan")
    pny = float("nan")
    pnz = float("nan")
    if args.pvx is not None: pvx = args.pvx
    if args.pvy is not None: pvy = args.pvy
    if args.pvz is not None: pvz = args.pvz
    if args.pnx is not None: pnx = args.pnx
    if args.pny is not None: pny = args.pny
    if args.pnz is not None: pnz = args.pnz

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

    run(ifile, dt, dx, dy, dz, pvx, pvy, pvz, pnx, pny, pnz, fevent, nevents, outtype, nrows, ncols)

if __name__ == "__main__":
    main()
