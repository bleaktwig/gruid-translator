# -*- coding: utf-8 -*-
# Gruid Translator by Bruno Benkel
# To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
# all copyright and related or neighboring rights to Gruid Translator.

"""
A list of constants used by the entire program. Mainly contains strings hardcoded as are defined in
GEMC, with some additional stuff to help standardize the program.
"""

# Usage strings.
IHELP   = "path of the gemc file to be processed."
THELP   = "length of each time step for the generated time series in ns."
XHELP   = "length of each row for each of the time series' matrices in cm."
YHELP   = "length of each column for each of the time series' matrices in cm."
ZHELP   = "length of each depth column for each of the detector's body time series' matrices in cm."
PVXHELP = "x position of the vertex for the detecting plane inside the detector's body."
PVYHELP = "y position of the vertex for the detecting plane inside the detector's body."
PVZHELP = "z position of the vertex for the detecting plane inside the detector's body."
PNXHELP = "x direction of the normal vector to the detecting plane inside the detector's body."
PNYHELP = "y direction of the normal vector to the detecting plane inside the detector's body."
PNZHELP = "z direction of the normal vector to the detecting plane inside the detector's body."
FHELP   = "event number of the first event in the gemc file that should be read. Note that "\
          "events are counted from 1 onward. Default is 1."
NHELP   = "number of events to read, counting from the file set with FEVENT. Set to 0 to read "\
          "until the end of file. Default is 0."
OHELP   = "type of output to be generated. Can be any integer from 1 to 5. Check the README for a "\
          "detailed description of each alternative. Default is 2."
RHELP   = "number of rows set in the gemc simulation. By default this is read from the "\
          "filename, but this argument can be set to override this behaviour."
CHELP   = "number of columns set in the gemc simulation. By default this is read from the "\
          "filename, but this argument can be set to override this behaviour."

# Paths, prefixes, etc.
OUTPREF = "out_"

# Generic strings used to identify banks by name in python code.
HBANK  = "header bank"
UHBANK = "user header bank"
IRBANK = "integrated raw bank"
IDBANK = "integrated digitized bank"
GPBANK = "generated particles bank"

# Strings hardcoded into input file.
S_HBANK     = " --- Header Bank --"
S_UHBANK    = " --- User Header Bank --"
S_IRBANK    = "   -- integrated true infos bank  (51, 0) --"
S_IDBANK    = "   -- integrated digitized bank  (52, 0) --"
S_GPBANK    = " --- Generated Particles Bank --"
S_EOE       = " ---- End of Event  ----"
S_PARTICLE  = "Particle"
S_HIT       = "Hit"
S_NHITS     = "nhits"
S_PID       = "pid"
S_VOL       = "id"
S_TID       = "tid"
S_HITN      = "hitn"
S_AVGX      = "avg_x"
S_AVGY      = "avg_y"
S_AVGZ      = "avg_z"
S_AVGT      = "avg_t"
S_EDEP      = "totEdep"
S_TRACKE    = "trackE"
S_PHOTONPID =    "0"
S_MMPID     =  "-13"
S_MPPID     =   "13"
S_EMPID     =   "11"
S_EPPID     =  "-11"
S_NPID      = "2112"

# Strings defined and used by this program.
S_EVENT       = "event"
S_GEMCMETA    = "gemc metadata"
S_GRUIDMETA   = "gruid metadata"
S_NROWS       = "# of rows (y)"
S_NCOLS       = "# of columns (x)"
S_NDCOLS      = "# of columns (z)"
S_PHOTONHITS  = "photon hits"
S_MASSHITS    = "massive particle hits"
S_MUONMHITS   = "muon- hits"
S_MUONPHITS   = "muon+ hits"
S_NEUTRONHITS = "neutron hits"
S_GRUIDHITS   = "gruid hits"
S_SIDE1       = "side 1"
S_SIDE2       = "side 2"
S_BODY        = "body"
S_DPLANE      = "detecting plane"
S_GRUIDNHITS  = "# of hits"
S_GRUIDEDEP   = "energy deposited"
S_PHOTONH1 = S_PHOTONHITS + " - " + S_SIDE1
S_PHOTONH2 = S_PHOTONHITS + " - " + S_SIDE2
S_GRUIDH1  = S_GRUIDHITS  + " - " + S_SIDE1
S_GRUIDH2  = S_GRUIDHITS  + " - " + S_SIDE2
S_GRUIDHB  = S_GRUIDHITS  + " - " + S_BODY
S_ID    = "tid"
S_N     = 'n'
S_X     = 'x'
S_Y     = 'y'
S_Z     = 'z'
S_T     = 't'
S_ED    = "Edep"
S_TRKE  = "TrkE"
S_DT    = "dt"
S_DX    = "dx"
S_DY    = "dy"
S_DZ    = "dz"

# IDs of the sensor endplates, as defined by the gemc simulation.
SENSOR1A_ID =  4
SENSOR2A_ID =  5
SENSOR1B_ID = 14
SENSOR2B_ID = 15

# Hardcoded measurements in the gemc simulation.
STRIP_RADIUS = 0.050
CORE_RADIUS  = 0.046
DZ           = 2. # core.depth/2 + sensor.depth

# Variables that depend on NROWS and NCOLS, variables that depend on the simulation conditions in
# the input file.
def NROWSA(NROWS): return (NROWS + 1)/2
def NROWSB(NROWS): return (NROWS - 1)/2
def DX(NCOLS): return (2.*STRIP_RADIUS * NCOLS)/2.
def DY(NROWS): return (2.*STRIP_RADIUS + (STRIP_RADIUS * (1.732050808 + 1)) * (NROWS - 1))/2.
