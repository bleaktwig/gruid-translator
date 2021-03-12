# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
A list of constants used by the entire program. Mainly contains strings hardcoded as are defined in
GEMC, with some additional stuff to help standardize the program.
"""

# Paths, prefixes, etc.
OUTPATH = "../out"
OUTPREF = "out_"

# Generic strings used to identify banks by name in python code.
HBANK  = "header bank"
UHBANK = "user header bank"
IRBANK = "integrated raw bank"
IDBANK = "integrated digitized bank"
GPBANK = "generated particles bank"

# Strings hardcoded into input file.
S_HBANK    = " --- Header Bank --"
S_UHBANK   = " --- User Header Bank --"
S_IRBANK   = "   -- integrated true infos bank  (51, 0) --"
S_IDBANK   = "   -- integrated digitized bank  (52, 0) --"
S_GPBANK   = " --- Generated Particles Bank --"
S_EOE      = " ---- End of Event  ----"
S_PARTICLE = "Particle"
S_HIT      = "Hit"
S_NHITS    = "nhits"
S_PID      = "pid"
S_VOL      = "id"
S_HITN     = "hitn"
S_AVGX     = "avg_x"
S_AVGY     = "avg_y"
S_AVGT     = "avg_t"
S_EDEP     = "totEdep"

# Strings defined and used by this program.
S_GEMCMETA = "gemc metadata"
S_GRUIDMETA = "event metadata"
S_NROWS = "nrows"
S_NCOLS = "ncols"
S_GEMCHITS  = "gemc hits"
S_GRUIDHITS = "gruid hits"
S_SIDE1 = "side 1"
S_SIDE2 = "side 2"
S_GEMCH1   = S_GEMCHITS   + " - " + S_SIDE1
S_GEMCH2   = S_GEMCHITS   + " - " + S_SIDE2
S_GRUIDH1   = S_GRUIDHITS + " - " + S_SIDE1
S_GRUIDH2   = S_GRUIDHITS + " - " + S_SIDE2
S_N     = 'n'
S_X     = 'x'
S_Y     = 'y'
S_T     = 't'
S_E     = 'E'
S_DT    = "dt"
S_DX    = "dx"
S_DY    = "dy"

# IDs of the sensor endplates, as defined by the gemc simulation.
SENSOR1A_ID =  4
SENSOR2A_ID =  5
SENSOR1B_ID = 14
SENSOR2B_ID = 15

# Hardcoded measurements in the gemc simulation.
STRIP_RADIUS = 0.050
CORE_RADIUS  = 0.046

# Variables that depend on NROWS and NCOLS, variables that depend on the simulation conditions in
# the input file.
def NROWSA(NROWS): return (NROWS + 1)/2
def NROWSB(NROWS): return (NROWS - 1)/2
def DELTAX(NCOLS): return (2.*STRIP_RADIUS * NCOLS)/2.
def DELTAY(NROWS): return (2.*STRIP_RADIUS + (STRIP_RADIUS * (1.732050808 + 1)) * (NROWS - 1))/2.
