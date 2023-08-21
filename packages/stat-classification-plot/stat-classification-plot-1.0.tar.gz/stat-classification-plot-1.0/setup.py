from setuptools import setup, find_packages

from stat_plot import __version__

dependency = [
    'numpy>=1.22.4',
    'matplotlib>=3.5.3',
    'scikit-learn>=1.3.0',
    'einops>=0.6.1'
]

extra_save = [
]

extra_show = [
]
    
extra_dev = [
    *dependency,
    *extra_save,
    *extra_show
]

setup(
    name='stat-classification-plot',
    version=__version__,

    url='https://github.com/Paramuths/stat-classification-plot-package',
    author='Paramuth Samuthrsindh',
    author_email='paramuths@gmail.com',

    packages=find_packages(),

    # dependency installed in general
    install_requires=[
        *dependency
    ],

    # dependency installed with specific keywordd
    extras_require={
        'dev': extra_dev,
    },

    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)