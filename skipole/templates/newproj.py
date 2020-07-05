
import os


# from skipole import the WSGIApplication class which will be used to create a wsgi
# application, and exception classes which you will need in your functions

from skipole import WSGIApplication, skis, FailPage, GoTo, ValidateError, ServerError, use_submit_list


# the framework needs to know the location of the projectfiles directory holding the project data
# and static files.

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))
PROJECT = 'newproj'

# This file newproj.py is initially also created under the projectfiles directory, however it does not
# need to be sited there, and can be moved and your code developed elsewhere. The above PROJECTFILES
# path is only needed to set the location of the support files used by the project, not code. 

# proj_data is an optional dictionary of values which you are free to use, it will be made
# available to your functions as the attribute 'skicall.proj_data'

PROJ_DATA={}


# Your code needs to provide your own version of the following three functions

# Minimal versions are provided below, you could either develop them here,
# or more usually, create further modules and packages and import them.


def start_call(called_ident, skicall):
    "When a call is initially received this function is called."
    return called_ident


# You may wish to apply the decorator '@use_submit_list' to the submit_data
# function below. See the skipole documentation for details.

@use_submit_list
def submit_data(skicall):
    "This function is called when a Responder wishes to submit data for processing in some manner"
    return


def end_call(page_ident, page_type, skicall):
    """This function is called at the end of a call prior to filling the returned page with skicall.page_data,
       it can also return an optional session cookie string."""
    return



# The above functions are required as arguments to the skipole.WSGIApplication object
# and will be called as required.

# create the wsgi application
application = WSGIApplication(project=PROJECT,
                              projectfiles=PROJECTFILES,
                              proj_data=PROJ_DATA,
                              start_call=start_call,
                              submit_data=submit_data,
                              end_call=end_call,
                              url="/")

# The application uses the projectfiles location to find and load json files
# which define the project, and also uses your functions to populate returned pages.

# The skis application must always be added, without skis you're going nowhere!
# The skis sub project serves javascript files required by the framework widgets.

skis_application = skis.makeapp(PROJECTFILES)
application.add_project(skis_application, url='/lib')

# The add_project method of application, enables the added sub application
# to be served at a URL which should extend the URL of the main 'root' application.
# The above shows the main application served at "/" and the skis library
# project served at "/lib"


#############################################################################
#
# You should remove everything below here when deploying and serving your
# finished application. The following lines are used to serve the project
# locally and add the skiadmin project for development.

# Normally, when deploying on a web server, you would follow the servers
# own documentation which should describe how to load a wsgi application.
# for example, using gunicorn3 by command line

# gunicorn3 -w 4 newproj:application

# Where gunicorn3 is the python3 version of gunicorn


if __name__ == "__main__":


    ############### THESE LINES ADD THE SKIADMIN SUB-PROJECT FOR DEVELOPMENT ONLY #
    ###################### AND SHOULD BE REMOVED WHEN YOU DEPLOY YOUR APPLICATION #

    from skipole import skiadmin, set_debug, skilift
    set_debug(True)
    skiadmin_application = skiadmin.makeapp(PROJECTFILES, editedprojname=PROJECT)
    application.add_project(skiadmin_application, url='/skiadmin')

    # serve the application with the development server from skilift

    host = "127.0.0.1"
    port = 8000
    print("Serving %s on port %s. Call http://localhost:%s/skiadmin to edit." % (PROJECT, port, port))
    skilift.development_server(host, port, application)
 

