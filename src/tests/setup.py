from distutils.core import setup, Extension

# the c++ extension module
extension_mod = Extension("shared_memory_python2", ["shared_memory_python2.c"])

setup(name = "shared_memory_python2", ext_modules=[extension_mod])

