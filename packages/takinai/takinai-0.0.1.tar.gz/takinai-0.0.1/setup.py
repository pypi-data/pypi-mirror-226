"""Setup script for takinai"""

import os.path
from setuptools import setup

# file directory
HERE = os.path.abspath(os.path.dirname(__file__))

# README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# setup everything
setup(
    name="takinai",
    version="0.0.1",
    description="The official Python library for the TakinAI API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/datamonet/takinai-python",
    author="DataMonet LLC",
    author_email="support@takin.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["takinai"],
    include_package_data=True,
    install_requires=[
        "importlib_resources",
    ],
    entry_points={"console_scripts": ["takinai=takinai.__main__:main"]},

)
