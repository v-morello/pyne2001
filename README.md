# pyne2001

A python wrapper around the original FORTRAN implementation of the NE2001 Galactic free electron density model, published in the paper  
[NE2001.I. A New Model for the Galactic Distribution of Free Electrons and its Fluctuations](https://arxiv.org/abs/astro-ph/0207156), by J.M. Cordes and T.J.W. Lazio.

**If using `pyne2001` contributes to a project that leads to a scientific publication, please cite the article above.**

The python functions implemented in `pyne2001` simply call the NE2001 executable and parse the resulting text output. This module uses version 1.0 of the FORTRAN code available from [http://hosting.astro.cornell.edu/~cordes/NE2001/](http://hosting.astro.cornell.edu/~cordes/NE2001/), with a few minor changes documented below (c.f. section "FORTRAN code changes"). **None of the changes affect the numerical results returned by the NE2001 program**, they are just minor bugfixes and quality-of-life changes to make the parsing of the text output easier.

### Dependencies and Python version

`pyne2001` works with both python 2.7 and python 3+, and does not depend on any external python libraries. You must have `gfortran` installed to compile the FORTRAN source; if you wish to use another compiler, you will have to install in development mode (see below) and edit the `Makefile` under `pyne2001/NE2001/src`.


### Installation

`pyne2001` can be installed easily with pip:
```bash
pip install pyne2001
```

To check that all went well, try importing the module and running the unit tests, you should see something like this:

```ipython
In [1]: import pyne2001

In [2]: pyne2001.test()
.......
----------------------------------------------------------------------
Ran 7 tests in 0.166s

OK
```

### Installation in development mode

If you want to be able to modify the code freely: clone the repository, then in its base folder type ```make install```. This compiles the FORTRAN code and runs ```pip install``` in [editable mode](https://pip.pypa.io/en/latest/reference/pip_install/#editable-installs).


### Usage

`pyne2001` provides 6 functions, see their docstrings for the full details:

- `get_dist`: Calculate the NE2001 distance for the given Galactic coordinates and DM. Returns a tuple `(dist_kpc, lim)` where `lim` is a boolean flag that is `True` if the returned distance value is only a lower limit estimate (i.e. input DM exceeds Galactic contribution).

- `get_dist_full`: Same as `get_dist`, but instead return the full NE2001 output as a dictionary. The keys are parsed from the second output column of the NE2001 program, see table below and original paper for further details.

- `get_dm`: Calculate the NE2001 DM for for the given Galactic coordinates and distance.

- `get_dm_full`: Same as `get_dm`, but instead return the full NE2001 output as a dictionary. The keys are parsed from the second output column of the NE2001 program, see table below and original paper for further details.

- `get_galactic_dm`: A convenience function to get the Galactic DM contribution for a given line of sight. Simply calls `get_dm` with `dist_kpc = 30.0`.

- `test`: Run all unit tests

The output keys when returning the full output are:
```
Key       Unit                     Description
------------------------------------------------------------
DIST      (kpc)                    ModelDistance
DM        (pc-cm^{-3})             DispersionMeasure
DMz       (pc-cm^{-3})             DM_Zcomponent
SM        (kpc-m^{-20/3})          ScatteringMeasure
SMtau     (kpc-m^{-20/3})          SM_PulseBroadening
SMtheta   (kpc-m^{-20/3})          SM_GalAngularBroadening
SMiso     (kpc-m^{-20/3})          SM_IsoplanaticAngle
EM        (pc-cm^{-6})             EmissionMeasure_from_SM
TAU       (ms)                     PulseBroadening @1GHz
SBW       (MHz)                    ScintBW @1GHz
SCINTIME  (s)                      ScintTime @1GHz @100 km/s
THETA_G   (mas)                    AngBroadeningGal @1GHz
THETA_X   (mas)                    AngBroadeningXgal @1GHz
NU_T      (GHz)                    TransitionFrequency
LOWERLIM                           If True, ModelDistance is a lower limit only
```


### FORTRAN code changes

##### Bugfixes:

- Removed extra space between declared `common` arrays  (`dmdsm.NE2001.f:68`)

- Replaced hardcoded `1` by `1.0` in a call to `max()` that needs two arguments of type float (`dmdsm.NE2001.f:408`)

- Replaced `iargc` by `iargc_` (`NE2001.f:28-29`)

- Replaced obsolete PAUSE statement with a WRITE (`density.NE2001.f:697`)

##### Changes:

- Input files are now all placed in `/bin`. Removed `/input` directory.

- Removed `run_NE2001.pl`

- FORTRAN code is now compiled with ```-ffpe-summary=none```, which suppresses messages related to floating point warnings. This makes parsing the output with python easier. (`Makefile`)

- Changed compiler from f77 to gfortran (`Makefile`)

- `make clean` now also deletes `libNE2001.a` (`Makefile`)