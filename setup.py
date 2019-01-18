import os
import setuptools
import subprocess
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py


def compile_ne2001():
    try:
        cwd = os.getcwd()
        thisdir, __ = os.path.split(__file__)
        srcdir = os.path.realpath(os.path.join(thisdir, 'pyne2001', 'NE2001', 'src'))
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


# NOTE: It is necessary to also have a custom build_py command
# During the first 'pip install' on a given machine, pip caches the packages
# with all its build files into a wheel (.whl). To do so, it runs the 
# 'build_py' command and stores all resulting files in the .whl. If
# 'build_py' does not call compile_ne2001(), then the .whl will NOT contain
# the compiled binaries. And in this case, running pip install another
# time (in another conda environment for example) actually installs that
# cached .whl which contains no binaries, and the module does not work.
class CustomBuildPy(build_py):
    def run(self):
        self.announce("Compiling NE2001 FORTRAN code")
        compile_ne2001()
        build_py.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='pyne2001',
    url='https://github.com/v-morello/pyne2001',
    author='Vincent Morello',
    author_email='vmorello@gmail.com',
    description='A simple python wrapper around the original FORTRAN implementation of the NE2001 Galactic free electron density model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.1',
    packages=setuptools.find_packages(),
    install_requires=[],
    license='MIT License',

    # NOTE (IMPORTANT): This means that everything mentioned in MANIFEST.in will be copied at install time 
    # to the package’s folder placed in 'site-packages'
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Fortran",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering :: Astronomy"
        ],
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
        'build_py': CustomBuildPy
        }
)
