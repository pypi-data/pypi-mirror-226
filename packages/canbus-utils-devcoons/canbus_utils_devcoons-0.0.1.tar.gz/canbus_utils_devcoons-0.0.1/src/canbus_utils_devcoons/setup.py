from setuptools import setup, Extension

sfc_module = Extension('canbus_utils', sources = ['module.cpp'])

setup(
    name='canbus_utils',
    version='1.0',
    description='Python Package with some canbus frame utilities',
    ext_modules=[sfc_module]
)