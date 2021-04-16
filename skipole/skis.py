
"""
This skis project is added to other projects and consists of javascript and
css files. As it is essentially a 'library' it is usually given a URL of /lib
when added - but this is not a necessity, just convention.

To use this module - in your own code you would normally create your own
'application' object and then call this module's makeapp function to produce
a 'skis_application'.

You would then add skis_application to your application using

from skipole import skis
skis_application = skis.makeapp()
application.add_project(skis_application, url='/lib')
"""

import os
from . import WSGIApplication

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))

def start_call(called_ident, skicall):
    "This project has no start_call functionality"
    return called_ident

def submit_data(skicall):
    "This project has no submit_data functionality"
    return

def end_call(page_ident, page_type, skicall):
    "This project has no end_call functionality"
    return

# As this project is not intended to run as a stand-alone service, a function
# is provided rather than an application object being immediately created.

def makeapp():
    """This function returns the skis application."""

    # The WSGIApplication created here is generally given a URL of "/lib"
    # when added to the root project using application.add_project

    return WSGIApplication('skis', PROJECTFILES, {}, start_call, submit_data, end_call)


