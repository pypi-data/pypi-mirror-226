# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

from os import system
system("pip install git+https://github.com/freiburgermsu/ModelSEEDpy.git")
# print("ModelSEEDpy is installed")

setup(
    name="commscores",
    version="0.0.2",
    description="A Python package for quantifying microbial interactions",
    long_description_content_type="text/x-rst",
    long_description=readme,
    author="Andrew Freiburger",
    author_email="andrewfreiburger@gmail.com",
    url="https://github.com/freiburgermsu/CommScores",
    license=license,
    packages=["commscores"],
    # package_dir = {'CommScores':'commscores'},
    package_data={"data": ["raw/at_leaf/*"],   # strangely neither of these directories are captured by the sdist
                  "notebooks": ["at_leaf/*"]},
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    include_package_data =True,
    keywords = ['microbiology', "community", "scores", "interaction", "syntrophy", "competition"],
    install_requires=[
        "optlang", "numpy", "deepdiff", "sigfig"
    ],
    project_urls={
        "Documentation": "https://commscores.readthedocs.io/en/latest/",
        "Issues": "https://github.com/freiburgermsu/CommScores/issues",
    },
)
