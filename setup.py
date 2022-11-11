import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skipole",
    version="5.5.0",
    author="Bernard Czenkusz",
    author_email="bernie@skipole.co.uk",
    description="A WSGI Application generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bernie-skipole.github.io/skipole/",
    packages=['skipole', 'skipole.ski', 'skipole.ski.responders', 'skipole.ski.validators', 'skipole.ski.widgets'],
    include_package_data=True,
    keywords='wsgi application web framework',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
)
