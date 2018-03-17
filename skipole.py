#!/usr/bin/env python3


####### SKIPOLE WEB FRAMEWORK ########
#
# skipole.py  - The Skipole web site builder
#
# This file is part of the Skipole web framework
#
# Date : 20130205
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2013 Bernard Czenkusz
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


"""
Enables a user to create a wsgi web service.
A project of web folders, pages and widgets can be built which call
your own Python functions to submit and receive widget parameters.
"""

import sys

# Check the python version
if sys.version_info[0] != 3 or sys.version_info[1] < 2:
    print("Sorry, your python version is not compatable")
    print("This program requires python 3.2 or later")
    print("Program exiting")
    sys.exit(1)


import os, argparse

import skipoles

# the name of the admin project
adminproj = skipoles.adminproj

# the directory where projectfiles are held
projectfiles = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projectfiles')
skipoles.set_projectfiles(projectfiles)


# Set up command line parser

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
description='Skipole WSGI application generator',
epilog='''
Enables a user to create a wsgi application which calls your
own Python functions to set web page widget parameters.

Typically a new project can be created with the call:
skipole.py
without any arguments.

And an existing project can be administered with:
skipole.py -s myprojectname
''')

parser.add_argument('--version', action='version', version=skipoles.version)

parser.add_argument("-p", "--port", type=int, dest="port", default=8000,
                  help="The port the web server will listen at, default 8000.")

parser.add_argument("-o", "--option", dest="option",
                  help="An optional value passed to your functions.")

parser.add_argument("-w", "--waitress", action='store_true', dest="waitress", default=False,
                  help="Serve project with the Waitress web server (python3-waitress is required).")

parser.add_argument("-s", "--skiadmin", action='store_true', dest="skiadmin", default=False,
                  help="Load the %s project to administrate the given project. With your browser call project_url/%s" % (adminproj,adminproj))


group = parser.add_mutually_exclusive_group()

group.add_argument("-a", "--add", dest="addproj", nargs=2, metavar=('PROJDIR','PROJNAME'),
                  help="From an external project directory, add the project (creates symlinks).")

group.add_argument("-c", "--copy", dest="cpproj", nargs=3, metavar=('NEWPROJDIR','NEWPROJNAME', 'SOURCEPROJNAME'),
                  help="Create a new project by copying an existing project.")

group.add_argument("-n", "--new", dest="newproj", nargs=2, metavar=('NEWPROJDIR','NEWPROJNAME'),
                  help="Create a new project with the given project directory and project name.")

group.add_argument("-r", "--remove", nargs=1, metavar=('PROJNAME',),
                  help="Remove the given project (deletes symlinks).")

group.add_argument("-i", "--import", dest="tarimport", nargs=2, metavar=('NEWPROJDIR','TARFILEPATH'),
                  help="Import a project tar.gz file.")

group.add_argument("-l", "--list", action='store_true', dest="listprojects", default=False,
                  help="List current projects, then exits.")

group.add_argument('project', nargs='?', default='',
                   help="An existing project name to run, and (if -s used) to administer.")

args = parser.parse_args()

port = args.port


if args.waitress:
    # This requires python3 version of the waitress web server to be
    # installed on your server, package 'python3-waitress' with debian
    try:
        from waitress import serve
    except:
        print("Unable to import waitress")
        sys.exit(1)
else:
    # As default use the Python library web server
    from wsgiref.simple_server import make_server

if not (args.addproj or args.skiadmin or args.remove or args.listprojects or args.newproj or args.option or args.project or args.cpproj or args.tarimport):
    # skipole.py has been called on its own, or just with a port option
    # create interactive session to build a new project
    admin_mode = True
    skipoles.set_debug(True)
    print("Do you wish to create a new project?")
    responce = input('Type Yes to proceed :')
    if responce != 'Yes':
        print("Try skipole.py -h to list options.\nCommand terminated.")
        sys.exit(0)
    plist = os.listdir(projectfiles)
    plist.sort()
    project = ''
    while True:
        project = input('Type a new project name :')
        if not (project.isalnum() and project.islower()):
            print("The project name must be lowercase alphanumeric")
            continue
        if (project == adminproj) or (project == skipoles.newproj) or (project == skipoles.libproj):
            print("Invalid project name")
            continue
        if project in plist:
            print("This project already exists")
            continue
        break
    print("A new project requires an empty project folder.")
    responce = input('Have you already created a folder? (Yes if you have):')
    if responce == 'Yes':
        # Take an existing folder path
        while True:
            path = input('Give the folder path:')
            path = os.path.abspath(os.path.expanduser(path))
            if not os.path.isdir(path):
                print("Folder not found.")
                continue
            break
    else:
        # create a new folder path
        print("A new folder will be created.")
        while True:
            path = input('Input a new folder path:')
            if not path:
                continue
            path = os.path.abspath(os.path.expanduser(path))
            if os.path.exists(path):
                print("This folder already exists!")
                continue
            os.mkdir(path)
            break
    projectcopy = ''
    if plist:
        while True:
            responce = input('Do you wish to copy an existing project? (Yes if you do):')
            if responce == 'Yes':
                print("Project List:")
                print(*plist, sep="\n")
                projectcopy = input('Project name to copy:')
                if projectcopy not in plist:
                    print("This project has not been recognized")
                    continue
            break
    print("Building project %s in folder %s" % (project, path))
    print("For future use - to run the project use 'skipole.py %s'" %(project,))
    print("Or to administer the project, use 'skipole.py -s %s'" %(project,))
    if projectcopy:
        # copy an existing project in directory and symlink it
        skipoles.copy_proj_to_symlink(path, projectcopy, project)
    else:
        # Create a new project in directory and symlink it
        skipoles.copy_newproj_to_symlink(path, project)

else:
    # take options from parser

    if args.newproj:
        project = args.newproj[1]
    elif args.addproj:
        project = args.addproj[1]
    elif args.cpproj:
        project = args.cpproj[1]  # new project to be created
    elif args.remove:
        project = args.remove[0]  # project to be removed
    else:
        project = args.project


    # List projects
    if args.listprojects:
        plist = os.listdir(projectfiles)
        plist.sort()
        if plist:
            print("Project List:")
            print(*plist, sep="\n")
        else:
            print("No projects available")
        parser.exit()

    # project tar file to be imported
    if args.tarimport:
        sympath = os.path.abspath(os.path.expanduser(args.tarimport[0]))
        if not os.path.exists(sympath):
            os.mkdir(sympath)
            print("New directory created,")
        tarfilepath = os.path.abspath(os.path.expanduser(args.tarimport[1]))
        try:
            project = skipoles.import_project(sympath, tarfilepath)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print("Exception raised in skipoles.import_project")
            print("Import failed but extracted data may remain under %s" % (sympath,))
            sys.exit(9)
        print("Project imported; run 'skipole.py -s %s' to administer the project." % (project,))
        sys.exit(0)

    if not project:
        print("Error - a project name is required")
        sys.exit(4)

    # Do checks on given project name

    if not (project.isalnum() and project.islower()):
        print("Error - the project name must be lower case alphanumeric only")
        sys.exit(3)

    if (project == adminproj) or (project == skipoles.newproj) or (project == skipoles.libproj):
        if args.remove:
            print("Error - %s should not be removed." % (project,))
            sys.exit(4)
        print("Warning - %s is a system project and should not normally be altered." % (project,))
        print("Are you sure you wish to continue?")
        responce = input('Type Yes to proceed :')
        if responce != 'Yes':
            print("Command terminated.")
            sys.exit(0)

    # Remove project
    if args.remove:
        try:
            skipoles.remove_project(project)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print("Exception raised in skipoles.remove_project")
            sys.exit(9)
        sys.exit(0)

    # add a project by creating symlinks to an external project directory
    if args.addproj:
        sympath = os.path.abspath(os.path.expanduser(args.addproj[0]))
        try:
            skipoles.make_symlink_to_project(sympath, project)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print("Exception raised in skipoles.make_symlink_to_project")
            sys.exit(9)
        print("Project %s added, at directory %s." % (project,sympath))
        sys.exit(0)

    project_path = os.path.join(projectfiles, project)

    if args.newproj:
        if os.path.isdir(project_path):
            print("Error - This project name - or at least the symlink %s already exists." % (project_path,))
            sys.exit(5)
        # Create a new project in directory and symlink it
        sympath = os.path.abspath(os.path.expanduser(args.newproj[0]))
        if not os.path.exists(sympath):
            os.mkdir(sympath)
            print("New directory created,")
        skipoles.copy_newproj_to_symlink(sympath, project)
        print("Project %s created." % (project,))
        sys.exit(0)

    if args.cpproj:
        # new project must not already exist
        if os.path.isdir(project_path):
            print("Error - This project name - or at least the symlink %s already exists." % (project_path,))
            sys.exit(5)
        # source project must exist
        if not os.path.isdir(os.path.join(projectfiles, args.cpproj[2])):
            print("Error - Project not found. Try 'skipole.py -l' option to list projects.")
            sys.exit(6)
        # Create a copy project in directory and symlink it
        sympath = os.path.abspath(os.path.expanduser(args.cpproj[0]))
        if not os.path.exists(sympath):
            os.mkdir(sympath)
            print("New directory created,")
        skipoles.copy_proj_to_symlink(sympath, args.cpproj[2], project)
        print("Project %s copied to %s." % (args.cpproj[2], project))
        sys.exit(0)

    # an existing project is to be loaded
    if not os.path.isdir(project_path):
        print("Error - Project not found. Try 'skipole.py -l' option to list projects.")
        sys.exit(6)

    if args.skiadmin:
        # set debug mode on
        admin_mode = True
        skipoles.set_debug(True)
    else:
        admin_mode = False


######################################
# create the site object
######################################

# If necessary, load the admin project
if admin_mode and (project != adminproj):
    adminprojectinstance = skipoles.load_project(adminproj, options = {}, rootproject = False)
    if adminprojectinstance is None:
        print("Admin project %s not found" % (adminproj,))
        sys.exit(8)

# An 'option' value can be passed to the project, and futher options to subprojects
# with a dictionary of {project:option,..} where each key is the project or sub project name
# and each option is any value you care to add, and which will appear as an argument in
# your start_call function. This allows you to pass a parameter from the command line, or from
# start up code set here, to your project code if required.
# If you do not wish to use this function, then pass an empty dictionary.

options = {project: args.option}

# create the wsgi application
try:
    application = skipoles.load_project(project, options)
except Exception as e:
    if hasattr(e, 'message'):
        print(e.message)
    else:
        print("Exception raised in skipoles.load_project")
    sys.exit(9)
    

if admin_mode and (project != adminproj):
    # and add the admin project to as a sub-project
    host = "127.0.0.1"
    application.add_project(adminprojectinstance)
    print("Administration at %s%s has been included." % (application.url, adminproj))
else:
    # remove the admin project
    application.remove_project(adminproj)
    host = ""

print("Serving project %s on port %s... open a browser and go to\nlocalhost:%s%s" % (project, port, port, application.url))

if admin_mode and (project != adminproj) :
    print("or to administer the site, go to\nlocalhost:%s%s%s" % (port, application.url, adminproj))

print("Press ctrl-c to stop.")


# serve the site

if args.waitress:
    if host:
        serve(application, host=host, port=port)
    else:
        serve(application, host='0.0.0.0', port=port)
else:
    # using the python wsgi web server
    httpd = make_server(host, port, application)
    httpd.serve_forever()






