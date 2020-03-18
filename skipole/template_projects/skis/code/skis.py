
# This skis project is added to other projects and consists of
# javascript and css files. As it is essentially a 'library'
# it is usually given a URL of /lib when added - but this is
# not a necessity, just convention.


from skipole import WSGIApplication

PROJECT = 'skis'

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

def makeapp(projectfiles, **proj_data):
    """This function returns the skis application."""

    # The WSGIApplication created here is generally given a URL of "/lib"
    # when added to the root project using application.add_project

    application = WSGIApplication(PROJECT, projectfiles, proj_data, start_call, submit_data, end_call)
    return application


############
#
#  To use this module - in your own code you would normally create your own 'application' object
#  and then call this module's makeapp function to produce a 'skis_application'
#  You would then add skis_application to your application using
#  application.add_project(skis_application, url='/lib')
#
#  The only difficulty is importing this module, however as skis.py should normally be in
#  PROJECTFILES/skis/code/skis.py
#  this directory can be added to the python path. So you would include
#  the following in your own code:
#
#  skis_code = os.path.join(PROJECTFILES, 'skis', 'code')
#  if skis_code not in sys.path:
#      sys.path.append(skis_code)
#  import skis
#  skis_application = skis.makeapp(PROJECTFILES)
#  application.add_project(skis_application, url='/lib')
#
############



