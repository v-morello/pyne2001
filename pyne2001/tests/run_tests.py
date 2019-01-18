import unittest
import os

def test():
    """ Run all unit tests """
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__))
    runner = unittest.TextTestRunner()
    runner.run(suite)