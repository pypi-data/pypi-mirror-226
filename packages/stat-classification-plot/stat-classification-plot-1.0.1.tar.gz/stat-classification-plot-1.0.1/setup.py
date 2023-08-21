from setuptools import setup, find_packages
from pathlib import Path

from stat_plot import __version__

# get the description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# specify the dependencies
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

    long_description=long_description,
    long_description_content_type='text/markdown',

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