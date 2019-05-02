import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skipole-bernieski",
    version="3.0.3",
    author="Bernard Czenkusz",
    author_email="bernie@skipole.co",
    description="A WSGI Aplication generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://skipole.bitbucket.io/",
    packages=['skipole', 'skipole.skilift', 'skipole.ski', 'skipole.ski.responders', 'skipole.ski.validators', 'skipole.ski.widgets'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)