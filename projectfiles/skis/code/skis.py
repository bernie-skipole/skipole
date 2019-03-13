# This skis project is added to other projects and consists of
# javascript and css files.


from skipole import WSGIApplication


def start_call(called_ident, skicall):
    "This project has no start_call functionality"
    return called_ident

def submit_data(skicall):
    "This project has no submit_data functionality"
    return

def end_call(page_ident, page_type, skicall):
    "This project has no end_call functionality"
    return


def makeapp(projectfiles, proj_data={}):
    """This function allows projectfiles and proj_data to be set into the skis application"""
    application = WSGIApplication('skis', projectfiles, proj_data, start_call, submit_data, end_call, url="/skis")
    return application


