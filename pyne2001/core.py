from __future__ import print_function
import os

try:
    # Python 3+
    from subprocess import getoutput
except ImportError:
    # Python 2
    from commands import getoutput


def _get_executable_dir():
    thisdir, __ = os.path.split(__file__)
    path = os.path.join(thisdir, "NE2001", "bin")
    return os.path.realpath(path)


executable_dir = _get_executable_dir()


def _run_ne2001(glon, glat, dmd, ndir):
    """
    dmd: float
        DM or distance in kpc, depending on ndir
    ndir: int
        If 1, convert DM to distance. If -1, convert distance to DM.
    """
    try:
        cwd = os.getcwd()
        os.chdir(executable_dir)
        out = None
        if dmd < 0:
            raise ValueError("dmd cannot be negative")
        if not ndir in (-1, 1):
            raise ValueError("ndir must be -1 or 1")

        cmd = "./NE2001 {:.6f} {:.6f} {:.6f} {:d}".format(glon, glat, dmd, ndir)
        out = getoutput(cmd)
    except Exception:
        raise
    finally:
        os.chdir(cwd)
    return out


def _parse_output(text):
    """ 
    Parse the output of the NE2001 program into a dictionary.
    """
    lines = [line.strip() for line in text.strip().splitlines()]
    lines = lines[6:] # Ignore comment lines and summary of inputs
    items = {}

    # Check for leading '>' character on first output line when NE2001 has
    # been called to convert DM to DIST. If '>' is there it means that the
    # output distance is only a lower limit
    items['LOWERLIM'] = False
    if lines[0].startswith('>') and 'DIST' in lines[0]:
        items['LOWERLIM'] = True
        lines[0] = lines[0].replace('>', ' ')        

    for line in lines:
        if not line.startswith("#"):
            lis = line.split()
            key = lis[1]
            val = float(lis[0])
            items[key] = val
    return items


def get_output(glon, glat, dmd, ndir):
    """ 
    Run the NE2001 program and parse its output into a dictionary.

    Parameters
    ----------
    glon: float
        Galactic longitude in degrees
    glat: float
        Galactic latitude in degrees
    dmd: float
        DM (pc cm^-3) or Distance (kpc) depending on the direction of conversion
        (see ndir parameter below)
    ndir: int
        If 1, convert DM to distance. If -1, convert distance to DM.

    Returns
    -------
    items: dict
        Dictionary with all output values. The keys are parsed from
        the second output column of the NE2001 program. 

    Raises
    ------
    ValueError:
        If dmd is negative or if ndir is not either -1 or 1
    RuntimeError: 
        If the output of the program cannot be parsed. This usually happens if
        the NE2001 programs returns an error message. In this case, the
        original text output of the program is returned as the message of the
        RuntimeError.
    """
    text = _run_ne2001(glon, glat, dmd, ndir)
    exc = None
    try:
        return _parse_output(text)
    except Exception as err:
        exc = err

    if exc:
        msg = "Failed to parse NE2001 output:\n{!s}".format(text)
        raise RuntimeError(msg)


def get_dm_full(glon, glat, dist_kpc):
    """ 
    Get the NE2001 model DM for given coordinates and distance, and return the
    full output from the program as a dictionary.

    Parameters
    ----------
    glon: float
        Galactic longitude in degrees
    glat: float
        Galactic latitude in degrees
    dist_kpc: float
        Distance in kpc

    Returns
    -------
    items: dict
        Dictionary with all the outputs of the NE2001 program
    """
    return get_output(glon, glat, dist_kpc, -1)


def get_dm(glon, glat, dist_kpc):
    """ 
    Get the NE2001 model DM for given coordinates and distance.

    Parameters
    ----------
    glon: float
        Galactic longitude in degrees
    glat: float
        Galactic latitude in degrees
    dist_kpc: float
        Distance in kpc

    Returns
    -------
    dm: float
        NE2001 model DM in pc cm^-3
    """
    return get_dm_full(glon, glat, dist_kpc)['DM']


def get_dist_full(glon, glat, dm):
    """ Get the NE2001 model distance for given coordinates and DM, and return
    the full output from the program as a dictionary.

    Parameters
    ----------
    glon: float
        Galactic longitude in degrees
    glat: float
        Galactic latitude in degrees
    dm: float
        DM in pc cm^-3

    Returns
    -------
    items: dict
        Dictionary with all the outputs of the NE2001 program
    """
    return get_output(glon, glat, dm, 1)


def get_dist(glon, glat, dm):
    """ Get the NE2001 model distance for given coordinates and DM.

    Parameters
    ----------
    glon: float
        Galactic longitude in degrees
    glat: float
        Galactic latitude in degrees
    dm: float
        DM in pc cm^-3

    Returns
    -------
    dist: float
        NE2001 model distance in kpc
    lower_limit: bool
        True if the distance returned is only a lower limit (input DM exceeds
        Galactic contribution), False otherwise.
    """
    items = get_dist_full(glon, glat, dm)
    return items['DIST'], items['LOWERLIM']


def get_galactic_dm(glon, glat):
    """ Get the Galactic DM contribution for given coordinates. This simply
    calls get_dm() with dist_kpc = 30.0.

    Parameters
    ----------
    glon: float
        Galactic longitude in degrees
    glat: float
        Galactic latitude in degrees

    Returns
    -------
    dm: float
        Galactic DM contribution in pc cm^-3
    """
    return get_dm(glon, glat, 30.0)
