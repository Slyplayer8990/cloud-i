from distutils.core import setup
from Cython.Build import cythonize

setup(
 ext_modules=cythonize("git.pyx"),
 ext_modules=cythonize("machines.pyx"),
 ext_modules=cythonize("k3s.pyx"),
 ext_modules=cythonize("storage.pyx")
)