import os
import setuptools
import subprocess
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop


def compile_ne2001():
    try:
        cwd = os.getcwd()
        thisdir, __ = os.path.split(__file__)
        srcdir = os.path.realpath(os.path.join(thisdir, 'NE2001', 'src'))
        os.chdir(srcdir)
        subprocess.check_call('make clean', shell=True)
        subprocess.check_call('make all', shell=True)
    except:
        raise
    finally:
        os.chdir(cwd)


class CustomInstall(install):
    def run(self):
        self.announce("Compiling NE2001 FORTRAN code")
        compile_ne2001()
        install.run(self)


class CustomDevelop(develop):
    def run(self):
        self.announce("Compiling NE2001 FORTRAN code")
        compile_ne2001()
        develop.run(self)


setup(
    name='pyne2001',
    url='https://github.com/v-morello/pyne2001',
    author='Vincent Morello',
    author_email='vmorello@gmail.com',
    description='A simple python wrapper around the original FORTRAN implementation of the NE2001 Galactic free electron density model',
    version='0.1.0',
    packages=setuptools.find_packages(),
    install_requires=[],
    license='MIT License',
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop
        }
)
