
# This skis project is added to other projects and consists of
# javascript and css files. As it is essentially a 'library'
# it is usually given a URL of /lib when added - but this is
# not a necessity, just convention.


from skipole import WSGIApplication, set_debug

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

    # The WSGIApplication created here has a URL of "/", however when this
    # application is added to another, it is generally given a URL of "/lib"
    # in the application.add_project method which overwrites the URL given here

    application = WSGIApplication(PROJECT, projectfiles, proj_data, start_call, submit_data, end_call, url="/")
    return application


# In normal use, the skis project is only imported, so the following is never run.
# However if you want to use skiadmin to modify skis, then it could be run like any other
# project. Please be aware new versions of skipole will include new versions of skis.
# Any changes you make to skis will be lost should you upgrade to a later version.


if __name__ == "__main__":

    # If called as a script, this portion runs the python wsgiref.simple_server

    import sys, os
    from wsgiref.simple_server import make_server

    PROJECTFILES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    application = makeapp(PROJECTFILES)

    set_debug(True)
    skiadmin_code = os.path.join(PROJECTFILES, 'skiadmin', 'code')
    if skiadmin_code not in sys.path:
        sys.path.append(skiadmin_code)
    import skiadmin
    skiadmin_application = skiadmin.makeapp(PROJECTFILES, editedprojname=PROJECT)
    application.add_project(skiadmin_application, url='/skiadmin')

    # serve the application
    host = "127.0.0.1"
    port = 8000

    httpd = make_server(host, port, application)
    print("Serving %s on port %s. Call http://localhost:%s/skiadmin to edit." % (PROJECT, port, port))
    httpd.serve_forever()

