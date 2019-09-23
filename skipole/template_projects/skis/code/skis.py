
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


