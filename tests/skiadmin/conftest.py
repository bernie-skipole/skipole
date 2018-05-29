##########################################################
#
# These tests are run using the python3 version of py.test
#
# which, when using debian, is the script py.test-3
# and with python3-pytest installed
#
# py.test-3 should be run from the 'skipole' directory
#
# This conftest.py file contains the fixture 'project'
# which loads the project to be tested into the framework
#
##########################################################

import os

import pytest

# the framework needs to know the directory where projectfiles are held
# which is normally 'projectfiles' beneath three directories up from this file

projectfiles = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'projectfiles')

@pytest.fixture(scope="session")
def project():
    """Sets the test project being run by skipole.
       Returns the project name"""
    import skipoles
    # this line sets the test project to 'skiadmin', and also
    # calls the user 'start_project' function
    testproject = skipoles.WSGIApplication("skiadmin", {}, projectfiles)
    return testproject.proj_ident


