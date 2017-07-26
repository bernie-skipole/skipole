# README #

skipole.py is a framework for creating wsgi applications.

A web admin interface allows the developer to create web pages containing widgets.

The developer then needs to write appropriate python functions to receive data and populate the widget parameters.

Skipole requires python 3.2 or later.

A new project can be created with the command:

skipole.py -n myprojectname

Or more typically, a pre-existing sample project can be copied, to take advantage of CSS classes applied to widgets. The copy command being:

skipole.py -c sampleproject myprojectname

Once created, the project can be administered with:

skipole.py -a myprojectname

This serves the application using the python standard library wsgiref.simple_server. Connecting to localhost:8000 will allow you to view the web site, and administer it at localhost:8000/skiadmin

It is intended that in a finished project the application could be served via any wsgi server.

The Downloads section of bitbucket.org/skipole/skipole contains the skipole tar file containing the framework, the latest version should be downloaded, extracted and the skipole.py script will be found within. Further information can be found from the wiki pages of this site, and the admin web interface contains its own documentation.
