

import os

# from skipole import the WSGIApplication class which will be used to create a wsgi application

from skipole import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, use_submit_list, skis, PageData, SectionData

# FailPage, GoTo, ValidateError and ServerError are exception classes which you can raise in your own code

# use_submit_list is a decorator described below

# skis is another skipole project which serves javascript files and its use is shown below

# PageData and SectionData are dictionary-like objects with attributes. Your code sets contents into
# these which will be applied to the page finally returned to the user.

# the framework needs to know the location of the projectfiles directory holding the project data
# and static files.

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))
PROJECT = "newproj"

# This file newproj.py is initially created under the projectfiles directory, however it does not
# need to be sited there, and can be moved and your code developed elsewhere. The above PROJECTFILES
# path is only needed to set the location of the support files used by the project, not code. 

# proj_data is an optional dictionary of values which you are free to use, it will be made
# available to your functions as the attribute 'skicall.proj_data'

PROJ_DATA={}


# Your code needs to provide your own version of the following three functions which will
# be used to set values into the widgets of returned pages. Minimal versions are provided below.

# When a call is received by the server, the framework converts the url called to a 'called_ident'
# which is a tuple (projectname, pagenumber), and then, if this is the project called, this
# start_call function is called. If the page called is not recognised, called_ident will be None.

# The skicall object has attributes and methods pertaining to the call. 


def start_call(called_ident, skicall):
    """When a call is initially received this function is called.
       Unless you want to divert to another page, this function should return called_ident
       which would typically be the ident of a Responder dealing with the call."""
    # to serve static files, you can map a url to a server static directory with the
    # skicall.map_url_to_server method, for example:
    # servedfile = skicall.map_url_to_server("images", "/home/user/thisproject/imagefiles")
    # if servedfile:
    #    return servedfile

    # Of particular interest at this point are the attributes:
    # skicall.received_cookies is a dictionary of cookie name:values received from the client
    # skicall.call_data is a dictionary which you can set with your own data and, as skicall is
    # passed on to the submit_data and end_call functions defined below, can be used to pass
    # data to these functions.

    # Normally you would return called_ident, which is the page being called, or None to cause a
    # page not found error, or another (project, pagenumber) to divert the call to another page.

    return called_ident

# After start_call, if the call is passed to a Responder page which you have set up to call
# submit_data, then the function below will be called.
#
# You may wish to apply the decorator '@use_submit_list' to the submit_data function. This
# takes the package, module and function name which you have set in the Responder's 'submit list'
# and imports and calls that specified function instead. This is entirely optional. 

def submit_data(skicall):
    """This function is called when a Responder wishes to submit data for processing in some manner
       Typically you would create a PageData object containing widget,field values and call the
       skicall.update method, where the data will be applied to the page returned"""
    # For example, if you have a page with a widget 'displaydata' and with a field 'hide' which you want
    # to set to True, you would use:
    #   pd = PageData()
    #   pd['displaydata','hide'] = True
    #   pd['otherwidgets', 'otherfields'] = 'Other values'
    # You may also have a section in the page, with a section alias of "mysection"
    #   sd = SectionData("mysection")
    #   sd['anotherwidget', 'widgetfield'] = "Text displayed on widget"
    # And then update pd with this section data
    #   pd.update(sd)
    # and finally, you would set the pd into skicall using update
    #   skicall.update(pd)

    return


def end_call(page_ident, page_type, skicall):
    """This function is called prior to returning a page,
       it can also be used to return an optional session cookie string."""
    # If you have created a PageData object and stored it in skicall.call_data
    # this would be a good place to call skicall.update(pd)
    # so the data is set into the page prior to returning the page to the user.
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


# Add the 'skis' application which serves javascript and css files required by
# the framework widgets.

# The skipole.skis package, contains the function makeapp() - which returns a
# WSGIApplication object which is then appended to your own project

skis_application = skis.makeapp()
application.add_project(skis_application, url='/lib')

# The add_project method of WSGIApplication enables the added sub application
# to be served at a URL which should extend the URL of the main 'root' application.
# The above shows the main application served at "/" and the skis library
# project served at "/lib"

# You can add further sub applications using the add_project method which has signature
# application.add_project(subapplication, url=None, check_cookies=None)
# The optional check_cookies argument can be set to a function which you would create, with signature:
# def my_check_cookies_function(received_cookies, proj_data):
# Before the call is routed to the subapplication, your my_check_cookies_function is called, with the
# received_cookies dictionary, and with your application's proj_data dictionary. If your function
# returns None, the call proceeds unhindered to the subapplication. If however your function returns
# an ident tuple, of the form (projectname, pagenumber), then the call is routed to that page instead.




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


    ############### THESE LINES ADD THE SKIADMIN SUB-PROJECT FOR DEVELOPMENT #
    ################# AND SHOULD BE REMOVED WHEN YOU DEPLOY YOUR APPLICATION #


    from skipole import skiadmin, set_debug, skilift
    set_debug(True)
    skiadmin_application = skiadmin.makeapp(editedprojname=PROJECT)
    application.add_project(skiadmin_application, url='/skiadmin')

    # serve the application with the development server from skilift

    host = "127.0.0.1"
    port = 8000
    print("Serving %s on port %s. Call http://localhost:%s/skiadmin to edit." % (PROJECT, port, port))
    skilift.development_server(host, port, application)
 


