from setuptools import setup, find_packages, Extension
import os


CYTHON_ERROR_MESSAGE = 'Cython>3.0.0 is required to install PySAIS'
NUMPY_ERROR_MESSAGE = 'numpy is required to install PySAIS'


try:
    import cython
except:
    print(CYTHON_ERROR_MESSAGE)
    raise


if int(cython.__version__[0]) < 3:
    raise ValueError(CYTHON_ERROR_MESSAGE)


try:
    import numpy as np
except:
    print(NUMPY_ERROR_MESSAGE)
    raise


from Cython.Build import cythonize


# Pick up a flag for the GLIBC fix.
glibc_fix = (False if 'GLIBC_FIX' not in os.environ else
             os.environ['GLIBC_FIX'] in
             {'Y', 'YES', 'y', 'yes', 'Yes', 'True', 'true', '1'})

compile_args = ['-O3', '-fomit-frame-pointer']
if glibc_fix:
    compile_args.append('-DGLIBC_FIX')

extensions = [Extension('PySAIS._sais32',
                        sources=['PySAIS/_sais32.pyx', 'PySAIS/sais32.c'],
                        include_dirs=[np.get_include()],
                        extra_compile_args=compile_args),
              Extension('PySAIS._sais64',
                        sources=['PySAIS/_sais64.pyx', 'PySAIS/sais64.c'],
                        include_dirs=[np.get_include()],
                        extra_compile_args=compile_args)]


setup(
    name='PySAIS',
    version='1.1.0',
    ext_modules=cythonize(extensions, include_path=[np.get_include()]),
    include_dirs=[np.get_include()],
    packages=find_packages(),
    install_requires=['Cython>=3.0.0', 'numpy', 'tables'],
    description='Suffix array computation with induced sorting algorithm.',
    long_description='PySAIS is a wrapper to Yuta Mori\'s implementation of '
                     'the induced sorting algorithm to create suffix arrays. '
                     'Both 32 bit and 64 bit indices are supported and '
                     'automatically recognised.\n\n'
                     'If you encounter a GLIBC_2.14 not found error, try '
                     're-installing with the environment variable GLIBC_FIX=1 '
                     'set.\n\n'
                     'Please raise issues on the tracker on bitbucket: '
                     'https://bitbucket.org/alex-warwickvesztrocy/pysais',
    license='MIT',  # Wrapped library is under MIT license.
    url='https://bitbucket.org/alex-warwickvesztrocy/pysais',
    author='Alex Warwick Vesztrocy',
    author_email='alex@warwickvesztrocy.co.uk'
)
