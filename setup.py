import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skipole",
    version="4.0.1",
    author="Bernard Czenkusz",
    author_email="bernie@skipole.co.uk",
    description="A WSGI Application generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bernie-skipole.github.io/skipole/",
    packages=['skipole', 'skipole.skilift', 'skipole.ski', 'skipole.ski.responders', 'skipole.ski.validators', 'skipole.ski.widgets',
              'skipole.skiadmin', 'skipole.skiadminpackages', 'skipole.skiadminpackages.editcss', 'skipole.skiadminpackages.editfiles',
              'skipole.skiadminpackages.editfolders', 'skipole.skiadminpackages.editpages', 'skipole.skiadminpackages.editparts',
              'skipole.skiadminpackages.editresponders', 'skipole.skiadminpackages.editsectionplaces', 'skipole.skiadminpackages.editsections',
              'skipole.skiadminpackages.editspecialpages', 'skipole.skiadminpackages.edittext', 'skipole.skiadminpackages.edittextblocks',
              'skipole.skiadminpackages.editvalidators', 'skipole.skiadminpackages.editwidgets'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
)
