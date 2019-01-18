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


if __name__ == "__main__":
    unittest.main()
