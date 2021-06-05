import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skipole",
    version="5.3.4",
    author="Bernard Czenkusz",
    author_email="bernie@skipole.co.uk",
    description="A WSGI Application generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bernie-skipole.github.io/skipole/",
    packages=['skipole', 'skipole.skilift', 'skipole.ski', 'skipole.ski.responders', 'skipole.ski.validators', 'skipole.ski.widgets',
              'skipole.skiadmin', 'skipole.skiadmin.skiadminpackages', 'skipole.skiadmin.skiadminpackages.editcss', 'skipole.skiadmin.skiadminpackages.editfiles',
              'skipole.skiadmin.skiadminpackages.editfolders', 'skipole.skiadmin.skiadminpackages.editpages', 'skipole.skiadmin.skiadminpackages.editparts',
              'skipole.skiadmin.skiadminpackages.editresponders', 'skipole.skiadmin.skiadminpackages.editsectionplaces', 'skipole.skiadmin.skiadminpackages.editsections',
              'skipole.skiadmin.skiadminpackages.editspecialpages', 'skipole.skiadmin.skiadminpackages.edittext', 'skipole.skiadmin.skiadminpackages.edittextblocks',
              'skipole.skiadmin.skiadminpackages.editvalidators', 'skipole.skiadmin.skiadminpackages.editwidgets'],
    include_package_data=True,
    keywords='wsgi application web framework',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
)
