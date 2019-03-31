# README #

skipole is a framework for creating wsgi applications. A web admin interface allows the developer to create web pages containing widgets.

Skipole requires python 3.2 or later.
 
The framework is used to create a project, this consists of a number of 'pages' generated by the framework that together with your own code will produce a wsgi application.

To create a new project you would normally run:

python3 -m skipole myproj /path/to/projectfiles

You should replace 'myproj' with your preferred name for a new project. A projectfiles directory will be created with your new project 'myproj' and myproj.py within it.

The framework provides a 'skiadmin' facility allowing you to create template pages of various types (html, css and svg) and also 'Responders' which are script 'pages' which call your functions defined in myproj.py

The developer runs

python3 /path/to/projectfiles/myproj/code/myproj.py

then connects with a browser to localhost:8000 to view the project, and calls localhost:8000/skiadmin to open an administrative site to add and edit folders and pages.

'pages' are of several types, the main ones being template and responder pages. Typically you populate the templates with widgets, and set up the responders to accept an incoming call, and then route data from the call to your own code in myproj.py. Your code sets data into a Python dictionary, which is set into a template page and returned to the caller.

Your Python functions in myproj.py are described in greater detail within the skiadmin pages. These functions would typically call further code of your own, to serve whatever data you require.

