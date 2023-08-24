# -*- coding: utf-8 -*-
from setuptools import setup
import os


# Setup!
setup(
    name="vplot",
    description="plotting tools for vplanet",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VirtualPlanetaryLaboratory/vplot/",
    author="Rodrigo Luger",
    author_email="rodluger@gmail.edu",
    license="MIT",
    packages=["vplot"],
    include_package_data=True,
    use_scm_version={
        "write_to": os.path.join("vplot", "vplot_version.py"),
        "write_to_template": '__version__ = "{version}"\n',
    },
    install_requires=[
        "setuptools_scm",
        "numpy>=1.19.2",
        "matplotlib>=3.3.4",
        "astropy>=4.1",
        "vplanet>=2.0.0",
    ],
    entry_points={
        "console_scripts": ["vplot=vplot.command_line:_entry_point"]
    },
    setup_requires=["setuptools_scm"],
    zip_safe=False,
)
