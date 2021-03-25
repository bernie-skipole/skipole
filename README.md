# README #

skipole is a framework for creating wsgi applications. A web admin interface, together with your own code, allows the developer to create dynamic web pages.

Skipole requires python 3.6 or later, and can be installed with:

python3 -m pip install skipole
 
### Starting a new project ###

To create a new project you would normally run:

python3 -m skipole myproj /path/to/projectfiles

You should replace 'myproj' with your preferred name for a new project. A projectfiles directory will be created with your new project 'myproj' within it.

You would then run:

python3 /path/to/projectfiles/myproj.py

then connect with a browser to localhost:8000 to view the project, and call localhost:8000/skiadmin to open an administrative site to add and edit folders and pages.

### Developing a project ###

The file myproj.py contains code which generates the wsgi application, and functions which you will develop further yourself.

The pages served at /skiadmin provide the web based admin facility allowing you to create template and responder pages. Typically you set up 'responders' to accept an incoming call which in turn calls your own functions defined in myproj.py. Your code sets data into a Python object, which is set into a template page and returned to the caller.

Your Python functions in myproj.py are described in greater detail within the skiadmin pages.

### Special features ###

The widget field values which you create are normally set into the returned template page, but they can also be set into a JSON file, which updates the widgets already displayed on the client browser. This enables facilities such as SVG meters and graphs to be dynamcally updated.

The widgets created have a look and feel set by CSS classes, you have the facility to set your own classes on the widgets to change their looks, and also to set 'default' classes on a per project basis.

### Final output ###

When you have fully developed your application, and wish to deploy it, you would remove the lines in myproj.py which run the development_server, and which add the skiadmin sub project, and you will be left with your final WSGI 'application' - which can be served by any wsgi compatable web server.

### Upgrading ###

To upgrade to the latest version:

python3 -m pip install --upgrade skipole

Check you have the latest with:

python3 -m skipole --version

### Further information ###

The web admin pages have extensive documentation and help features, and for further information go to:

https://bernie-skipole.github.io/skipole


