# Gruid Translator
Gruid Translator is a small tool in Python that attempts to convert a GEMC simulation of a generic
calorimeter detector to a format more similar to how the output is seen in real life.

Taking a .txt file exported by [bcal_generator](https://github.com/emolinac/bcal), this tool
generates a time series of sparse matrices detailing the location and energy deposited of hits in
the scintillating fibers.
It can also export these matrices as .json files for easy loading.

#### Units
* **Energy** is measured in **MeV**.
* **Distance** is measured in **cm**.
* **Time** is measured in **ns**.

## Usage
Just clone and run `run.sh` with Python 3.9+ or above.
The program requires four positional arguments to run, with more parameters available as optional
arguments.

```
usage: main.py [-h] [-z DZ] [--pvx PVX] [--pvy PVY] [--pvz PVZ] [--pnx PNX] [--pny PNY] [--pnz PNZ]
               [-f FEVENT] [-n NEVENTS] [-o OUTTYPE] [-r NROWS] [-c NCOLS]
               filename dt dx dy

positional arguments:
  filename              path of the gemc file to be processed.
  dt                    length of each time step for the generated time series in ns.
  dx                    length of each row for each of the time series' matrices in cm.
  dy                    length of each column for each of the time series' matrices in cm.

optional arguments:
  -h, --help            show this help message and exit
  -z DZ, --dz DZ        length of each depth column for each of the detector's body time series' matrices in cm.
  --pvx PVX             x position of the vertex for the detecting plane inside the detector's body.
  --pvy PVY             y position of the vertex for the detecting plane inside the detector's body.
  --pvz PVZ             z position of the vertex for the detecting plane inside the detector's body.
  --pnx PNX             x direction of the normal vector to the detecting plane inside the
                        detector's body.
  --pny PNY             y direction of the normal vector to the detecting plane inside the
                        detector's body.
  --pnz PNZ             z direction of the normal vector to the detecting plane inside the
                        detector's body.
  -f FEVENT, --fevent FEVENT
                        event number of the first event in the gemc file that should be read. Note
                        that events are counted from 1 onward. Default is 1.
  -n NEVENTS, --nevents NEVENTS
                        number of events to read, counting from the file set with FEVENT. Set to 0
                        to read until the end of file. Default is 0.
  -o OUTTYPE, --outtype OUTTYPE
                        type of output to be generated. Can be any integer from 1 to 5. Check the
                        README for a detailed description of each alternative. Default is 2.
  -r NROWS, --nrows NROWS
                        number of rows set in the gemc simulation. By default this is read from the
                        filename, but this argument can be set to override this behaviour.
  -c NCOLS, --ncols NCOLS
                        number of columns set in the gemc simulation. By default this is read from
                        the filename, but this argument can be set to override this behaviour.
```

`OUTTYPE` requires a more elaborate description:
* `1`: print the generated `.json` to `stdout`, mainly for testing.
This option can generate a truckload of output, so use with caution!
* `2`: A `.json` file containing the time series is stored in `out/`.
This is the default option.
* `3`: The massive particle hits are added to the exported file.
These are the targets for reconstruction.
* `4`: The photon hits used to generate the time series are added to the exported file.
This can aid in debugging.
* `5`: The metadata taken from the GEMC input file is added to the `.json` file.
This can be useful if the user wants to destroy this file or take some info from it.

Due to the programmer's laziness, the program requires `numpy` to be installed.
Sorry!

## Output Format
The `.json` file generated follows a very simple format.

The first keys contain the name of the input file and the event number.
The filename is included in case the user wants to merge various generated `.json` files.

The amount of second keys vary depending on the `OUTTYPE` set to generate them.
Each of these and their following keys are listed here:
* **gruid metadata**: metadata for the time series generated, added to simplify the user's life.
Contains the `dt`, `dx`, `dy`, `dz`, and the number of rows and columns in the generated matrices
for that event.
* **gruid hits - side n**: hits in the "standard gruid format" for one detector side (**n** can be 1
or 2).
The following keys are the instants of time for the time series.
Following these, the keys are in a format (`x,y`), representing the position in the generated
matrix, and their value is the deposited energy **in MeV**.
* **gruid hits - body**: hits in the "standard gruid format" for the body of the detector.
To store information about the detector's depth, is a 3-dimensional matrix.
The following keys are the instants of time for the time series.
Following these, the keys are in a format (`x,y,z`), representing the position in the generated
matrix, and their value is a list of hits which includes the PID of the particle involved and its
deposited energy.
* **muon hits**: Contains all the muon hits registered in the event.
`n` is the hit number (as defined by gemc), `t` the time in ns, `x` and `y` the position in cm, and
`E` the energy deposited in MeV.
* **photon hits - side n**: photon hits to the detecting surfaces in the event.
Only present for debugging purposes.
Follows the same standard as the muon hits.
* **gemc metadata**: All the metadata contained in the input GEMC file.
Could be useful to replicate the conditions in the original simulation.
The PID in this metadata is the PID of the incoming particle.

## Contributing
Pull requests are welcome, but please open an issue first if you would like to make a large change.
If I seem to ignore your pull request and/or issue, please email me at
[bruno.benkel@gmail.com](mailto:bruno.benkel@gmail.com).

## License
To the extent possible under law, the person who associated CC0 with Gruid Translator has waived
all copyright and related or neighboring rights to Gruid Translator.

[CC0](https://creativecommons.org/share-your-work/public-domain/cc0/)
