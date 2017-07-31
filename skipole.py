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
from wsgiref.simple_server import make_server

import skipoles

# the name of the admin project
adminproj = skipoles.adminproj

# the directory where projectfiles are held
projectfiles = skipoles.projectfiles


# Set up command line parser

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
description='Skipole web framework',
epilog='''
Enables a user to create a wsgi application which calls your
own Python functions to set web page widget parameters.

Typically a new project can be created with the call:
skipole.py
without any arguments.

And an existing project can be administered with:
skipole.py -a myprojectname
''')

parser.add_argument("-p", "--port", type=int, dest="port", default=8000,
                  help="The port the web server will listen at, default 8000.")

parser.add_argument("-o", "--option", dest="option",
                  help="An optional value passed to your functions.")

parser.add_argument("-s", "--symlink", dest="symlink",
                  help="Move project to a (pre-existing and empty) external directory, and create symbolic links.")

parser.add_argument("-S", "--SYMLINK", dest="SYMLINK",
                  help="From an external project directory, add the project with symbolic links.")

parser.add_argument("-c", "--copy", dest="source",
                  help="Create a new project by copying an existing project.")

parser.add_argument("-n", "--new", action='store_true', dest="new", default=False,
                  help="Create a new project with the given project name.")

parser.add_argument("-d", "--delete", action='store_true', dest="delete", default=False,
                  help="Delete the given project.")

parser.add_argument("-i", "--import", dest="tarimport",
                  help="Import a project tar.gz file.")

parser.add_argument("-a", "--admin", action='store_true', dest="admin", default=False,
                  help="Load the admin project to administrate the given project. With your browser call project_url/%s" % (adminproj,))

parser.add_argument("-l", "--list", action='store_true', dest="listprojects", default=False,
                  help="List current projects, then exits.")

parser.add_argument('--version', action='version', version=('%(prog)s ' + skipoles.version))

parser.add_argument('project', nargs='?', default='',
                   help="A project name (lowercase, no funny characters). Either an existing project, or, with the -n argument, a new project to be created.\nNot used with -l or -i options")

args = parser.parse_args()

port = args.port

if not (args.SYMLINK or args.admin or args.delete or args.listprojects or args.new or args.option or args.project or args.source or args.symlink or args.tarimport):
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
    print("Or to administer the project, use 'skipole.py -a %s'" %(project,))
    if projectcopy:
        # copy an existing project in directory and symlink it
        skipoles.copy_proj_to_symlink(path, projectcopy, project)
    else:
        # Create a new project in directory and symlink it
        skipoles.copy_newproj_to_symlink(path, project)

else:
    # take options from parser
    project = args.project

    if args.listprojects and (project or args.delete or args.new or args.admin or args.tarimport or args.symlink or args.SYMLINK or args.source):
        parser.error("The -l/--list option cannot be used with any other option.")

    if args.symlink and (args.delete or args.admin or args.tarimport or args.SYMLINK):
        parser.error("The -s/--symlink option can only be used with a directory path and project name, with only -n and -c options allowed.")

    if args.SYMLINK and (args.delete or args.new or args.admin or args.tarimport or args.source or args.symlink):
        parser.error("The -S/--SYMLINK option can only be used with a directory path, and project name, not with any other option.")

    if args.source and (args.delete or args.new  or args.admin or args.tarimport):
        parser.error("The arguments combination is invalid")

    if args.tarimport and (project or args.delete or args.new or args.admin):
        parser.error("The -i/--import option can only be used with a path to a tar file")


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
        skipoles.import_project(args.tarimport)
        sys.exit(0)

    if not project:
        print("Error - a project name is required")
        sys.exit(4)

    # Do checks on given project name

    if not (project.isalnum() and project.islower()):
        print("Error - the project name must be lower case alphanumeric only")
        sys.exit(3)

    if (project == adminproj) or (project == skipoles.newproj) or (project == skipoles.libproj):
        if args.delete:
            print("Error - %s should not be deleted." % (project,))
            sys.exit(4)
        print("Warning - %s is a system project and should not normally be altered." % (project,))
        print("Are you sure you wish to continue?")
        responce = input('Type Yes to proceed :')
        if responce != 'Yes':
            print("Command terminated.")
            sys.exit(0)

    # symlink an existing project
    if args.symlink and (not args.new) and (not args.source):
        skipoles.make_symlink_from_project(args.symlink, project)
        sys.exit(0)

    # symlink an external project directory
    if args.SYMLINK:
        skipoles.make_symlink_to_project(args.SYMLINK, project)
        sys.exit(0)

    # Delete project
    if args.delete:
        skipoles.delete_project(project)
        sys.exit(0)

    project_path = os.path.join(projectfiles, project)

    if args.new or args.source:
        # new project is to be created
        if os.path.isdir(project_path):
            print("Error - This project name - or at least the directory %s already exists." % (project_path,))
            sys.exit(5)
    else:
        # an existing project is to be loaded
        if not os.path.isdir(project_path):
            print("Error - Project not found. Try 'skipole.py -l' option to list projects.")
            sys.exit(6)

    if args.new:
        if args.symlink:
            # Create a new project in directory and symlink it
            skipoles.copy_newproj_to_symlink(args.symlink, project)
        else:
            # Create a new project
            skipoles.copy_newproj_to(project)
        print("Project %s created." % (project,))
        sys.exit(0)

    if args.source:
        if args.symlink:
            # Create a copy project in directory and symlink it
            skipoles.copy_proj_to_symlink(args.symlink, args.source, project)
        else:
            # create new project by copying an existing project
            skipoles.copy_proj(args.source, project)
        print("Project %s copied to %s." % (args.source, project))
        sys.exit(0)

    if args.admin:
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

# load the project
site = skipoles.load_project(project, options)

if admin_mode and (project != adminproj):
    # and add the admin project to the site as a sub-project
    host = "127.0.0.1"
    site.add_project(adminprojectinstance)
    print("Administration at %s%s has been included." % (site.url, adminproj))
else:
    # remove the admin project
    site.remove_project(adminproj)
    host = ""

###################################################
# Run the project in a web server
###################################################

def application(environ, start_response):
    "Defines the wsgi application"
    status, headers, data = site.respond(environ)
    start_response(status, headers)
    return data

# serve the site
httpd = make_server(host, port, application)

print("Serving project %s on port %s... open a browser and go to\nlocalhost:%s%s" % (project, port, port, site.url))

if admin_mode and (project != adminproj) :
    print("or to\nlocalhost:%s%s%s\nto administer the site." % (port, site.url, adminproj))

print("Press ctrl-c to stop.")

if admin_mode:
    print("Be sure to commit the project first to save any changes.")

# Serve until process is killed
httpd.serve_forever()




