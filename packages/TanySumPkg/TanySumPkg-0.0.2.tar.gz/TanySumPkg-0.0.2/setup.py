from setuptools import setup, find_packages
import os

VERSION = '0.0.2'
DESCRIPTION = 'Sum Example for Packaging Practice'

# Setting up
setup(
    name="TanySumPkg",
    version=VERSION,
    author="Ritesh Patil",
    author_email="<patil.ritesh311@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)