import os
import codecs
import re
from setuptools import setup, find_packages



# from pathlib import Path

# Package meta-data.
NAME = 'CausalRec'
DESCRIPTION = 'An implementation to use Causal models to recommend the best.... '
URL = 'https://github.com/vntuyen/'
EMAIL = 'tuyen.vu@mymail.unisa.edu.au'
AUTHOR = 'Tuyen Vu'
LICENSE = "MIT License"


with open("README.md", "r") as readme_file:
    readme = readme_file.read()


# Current Directory
try:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
except:
    CURRENT_DIR = os.path.dirname(os.path.realpath('__file__')) + '/'
print(CURRENT_DIR),



def read_version(*file_paths):
    with codecs.open(os.path.join(CURRENT_DIR, *file_paths), 'r') as fp:
        version_file = fp.read()

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name=NAME,
      version=read_version("CausalRec", "__init__.py"),
      description=DESCRIPTION,
      long_description= readme,
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license=LICENSE,
      packages=find_packages(),
      setup_requires=["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.0"],
      # install_requires=requirements,
      # install_requires=install_requires(),
      install_requires=['pathlib >= 1.0',       # Mar 26, 2014
                        'pandas >= 1.0.0',      # Jan 30, 2020
                        'matplotlib >= 3.3.0',  # Jul 17, 2020
                        'anytree >= 2.7.0',     # Sep 25, 2019
                        'scipy >= 1.5.0',       # Jun 22, 2020
                        'scikit-learn >= 0.23.0', # May 13, 2020
                        'numpy >= 1.19.0',      # Jun 21, 2020
                        'sphinx >= 4.0.0'       # May 9, 2021  There are many versions till now
                        ],
      package_data={ '': ['*.csv', '*.r', '*.R', '*.txt'],
                    "input": ["*.csv"],
      },
      include_package_data=True,
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Operating System :: MacOS',
          'Operating System :: Unix',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering',
		  'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      )
