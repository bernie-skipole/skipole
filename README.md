# README #

skipole.py is a framework which enables a user to create a wsgi application via a web admin interface for templates and widgets. The user then creates python functions to populate the widget parameters. It requires python 3.2 or later.

Typically a new project can be created with the call:

skipole.py -n myprojectname

Once created, the project can be administered with:

skipole.py -a myprojectname

This serves the project using the python standard library wsgiref.simple_server.

(The -n option creates a new project, the -a option starts the administration service.)

Connecting to localhost:8000 will allow you to view the application, and administer it at localhost:8000/skiadmin

Stop the server with ctrl-c

It is intended that in a finished project the application could be served via any wsgi server. The wiki pages of this site describe how nginx and uwsgi can be set up on a Debian based OS to automatically serve your application on power-up. 

The Downloads section of bitbucket.org/skipole/skipole contains the skipole tar file containing the framework, the latest version should be downloaded, extracted and the skipole.py script will be found within. Further information can be found from the wiki pages of this site, and the admin web interface contains its own documentation.