import unittest
from pyne2001 import *


class TestFunctions(unittest.TestCase):
    """ """
    def test_get_dm(self):
        get_dm(0, 0, 10.0)
    
    def test_get_dm_full(self):
        items = get_dm_full(0, 0, 10.0)

    def test_get_dist(self):
        get_dist(0, 0, 400.0)
    
    def test_get_dist_full(self):
        items = get_dist_full(0, 0, 400.0)

    def test_get_galactic_dm(self):
        get_galactic_dm(0, 0)

    def test_inversion1(self):
        glon = 5.0
        glat = 5.0
        dist_kpc = 1.0
        dm = get_dm(glon, glat, dist_kpc)
        dist_kpc_calculated, __ = get_dist(glon, glat, dm)
        self.assertAlmostEqual(dist_kpc, dist_kpc_calculated, places=3)

    def test_inversion2(self):
        glon = 10.0
        glat = 10.0
        dm = 100.0
        dist_kpc, __ = get_dist(glon, glat, dm)
        dm_calculated = get_dm(glon, glat, dist_kpc)
        self.assertAlmostEqual(dm, dm_calculated, places=3)

    def test_get_dm_ffpe(self):
        """ Run get_dm() for a high Galactic latitude line of sight and
        a high DM to trigger some floating point exceptions. 
        
        Here the raw NE2001 output may contain at the something like:
        'Note: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL'
        """
        get_dm(180.0, 80.0, 100.0)

    def test_get_dist_ffpe(self):
        """ Run get_dist() for a high Galactic latitude line of sight and
        a high distance to trigger some floating point exceptions. 
        
        Here the raw NE2001 output may contain at the end something like:
        'Note: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL'
        """
        get_dist(180.0, 80.0, 100.0)

    def test_get_dm_excessive(self):
        """ Run get_dm() for a high Galactic latitude line of sight and
        a VERY high DM to trigger the 'STOP loop limit' error of the NE2001
        executable.
        """
        with self.assertRaises(RuntimeError):
            get_dm(180.0, 80.0, 3000.0)

    def test_get_galactic_dm_centre(self):
        """ Check the numerical value of get_galactic_dm() for 
        coordinates (0, 0) """
        self.assertAlmostEqual(
            get_galactic_dm(0, 0), 
            3395.8779,
            places=2
            )

    def test_get_galactic_dm_anticentre(self):
        """ Check the numerical value of get_galactic_dm() for 
        coordinates (180, 0) """
        self.assertAlmostEqual(
            get_galactic_dm(180, 0), 
            188.2605,
            places=2
            )
    
    def test_get_dm_lowdist(self):
        """ Check that a ValueError is raised for DM input below 1e-6 """
        with self.assertRaises(ValueError):
            get_dm(0, 0, 1e-7)

    def test_get_dist_lowdm(self):
        """ Check that a ValueError is raised for dist input below 1e-6 """
        with self.assertRaises(ValueError):
            get_dist(0, 0, 1e-7)


if __name__ == "__main__":
    unittest.main()
