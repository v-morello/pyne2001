# Changelog
All notable changes will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.1.3 - 2019-01-26
### Changed
- Use the `FC` environment variable as the FORTRAN compiler, instead of enforcing `FC = gfortran` in `Makefile`
- Removed `-ffpe-summary=none` compilation option, to remain compatible with gfortran version <= 4

### Added
- Input DM or distance now enforced to be > 1e-6, because NE2001 executable hangs on zero (or close to zero) input.
- More unit tests

## 0.1.2 - 2019-01-24
### Added
- Version number is now specified in a unique location (`_version.py`) and can be accessed by the user as `pyne2001.__version__`

## 0.1.1 - 2019-01-18
### Added
- Can now be installed easily via `pip`. Directory structure has been modified as a result.

## 0.1.0 - 2019-01-09
### Added
- First release of pyne2001