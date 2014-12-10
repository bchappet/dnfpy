from distutils.core import setup, Extension
import numpy
setup(name='cmod', version='1.0',  \
      ext_modules=[Extension('cmod', ['testNumpy.c'],
              include_dirs=[numpy.get_include()]),
              ],
      )
