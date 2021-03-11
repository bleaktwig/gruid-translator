# The contents of this file is free and unencumbered software released into the
# public domain. For more information, please refer to <http://unlicense.org/>

"""
A list of constants used by the entire program. Mainly contains strings hardcoded as are defined in
GEMC, with some additional stuff to help standardize the program.
"""

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
S_HITN     = "hitn"
S_VOL      = "id"
S_X        = "avg_x"
S_Y        = "avg_y"
S_T        = "avg_t"
S_E        = "totEdep"

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
