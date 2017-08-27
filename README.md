# README #

skipole.py is a framework for creating wsgi applications.

A web admin interface allows the developer to create web pages containing widgets.

The developer then needs to write appropriate python functions to receive data and populate the widget parameters.

Skipole requires python 3.2 or later.

A new project can be created with the command:

python3 skipole.py

This creates and serves a new project using the python standard library wsgiref.simple_server. Connecting to localhost:8000 will allow you to view the web site, and administer it at localhost:8000/skiadmin

To serve and administer an already existing project, run:

python3 skipole.py -a myprojectname

It is intended that in a finished project the application could be served via any wsgi server.

The framework is available as a tar file in the Downloads section. It can be downloaded, extracted and the skipole.py script will be found within, it has no dependencies other than python 3.2 or above. So far it has been developed on Linux only, may work on Windows, not sure!

Further information can be found from the wiki pages of this site, and the admin web interface contains its own documentation.
