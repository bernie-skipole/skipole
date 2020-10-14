#
# This script is meant to be run from the command line using
#
# python3 -m skipole mynewproj /path/to/projectfiles
#
#

import sys, os, re, shutil

from . import version

DESCRIPTION = """Usage is

python3 -m skipole mynewproj /path/to/projectfiles

Which creates a directory /path/to/projectfiles
containing a sub directy and a python file:

mynewproj.py - a minimal python file which you willdevelop further.

mynewproj - a subdirectory containing data and static files for your new project

You should replace 'mynewproj' with your preferred name for a new project.

The path "/path/to/projectfiles" must be given, and is the path to a directory
where you will develop your project. Multiple projects can be created in one
'projectfiles' directory, or you could have multiple such directories holding
different projects.

If mynewproj already exists in the directory, it will not be changed.
"""


# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')


args = sys.argv

if len(args) == 3:
    project_name = args[1]
    if args[2].startswith('-'):
        print("Invalid filepath. " + DESCRIPTION)
        sys.exit(3)
    projectfiles = os.path.abspath(os.path.expanduser(args[2]))
    if _AN.search(project_name):
        print( "Error: Invalid project name, alphanumeric only")
        sys.exit(1)
    if '_' in project_name:
        print( "Error: Invalid project name, alphanumeric only (no underscore).")
        sys.exit(1)
    if (project_name == 'skis') or (project_name=='skiadmin'):
        print("Error: This project name is reserved")
        sys.exit(2)
elif len(args) == 2:
    if args[1] == "--version":
        print(version)
        sys.exit(0)
    elif (args[1] == "-h") or (args[1] == "--help"):
        print(DESCRIPTION)
        sys.exit(0)
    else:
        print("Unrecognised option. " + DESCRIPTION)
        sys.exit(3)
else:
    print( "Invalid input. " + DESCRIPTION)
    sys.exit(3)


# get the location of the directories to be copied
template_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')

template_newproj_directory = os.path.join(template_directory, 'newproj')
if not os.path.isdir(template_newproj_directory):
    print("Error: Cannot find the template data for the newproj project")
    sys.exit(7)
template_newproj_pyfile = os.path.join(template_directory, 'newproj.py')
if not os.path.isfile(template_newproj_pyfile):
    print("Error: Cannot find the template data for the newproj project")
    sys.exit(8)


project_directory = os.path.join(projectfiles, project_name)
project_pyfile = os.path.join(projectfiles, project_name + ".py")

# newproj python file
newproj_pyfile = os.path.join(projectfiles, 'newproj.py')


# If the given projectfiles directory does not exist
if not os.path.isdir(projectfiles):

    # create the directory by copying the template_directory
    shutil.copytree(template_directory, projectfiles)

    # new directory which has been created
    newproj_directory = os.path.join(projectfiles, 'newproj')

    # change the name of the newproj_directory to project_name
    os.rename(newproj_directory, project_directory)
else:
    # The given projectfiles does exist, so use it for the new project

    if os.path.isdir(project_directory) or os.path.isfile(project_pyfile):
        print("Project %s already exists, and has not been altered." % (project_name,))
        sys.exit(0)

    # create a new project
    shutil.copytree(template_newproj_directory, project_directory)
    shutil.copyfile(template_newproj_pyfile, newproj_pyfile)


# new_code_path -> project_pyfile
# newproj_file -> newproj_pyfile


print("Creating %s" % (project_pyfile,))

# change newproj.py to project_name.py, including the contents
## READ newproj.py

with open(newproj_pyfile, "r") as tnf:
    templatecontents = tnf.read()
os.remove(newproj_pyfile)
## REPLACE newproj with the new project name
newcontents = templatecontents.replace("newproj", project_name)
## REPLACE the 'os.path.dirname(os.path.realpath(__file__))' call with the new projectfiles
newcontents = newcontents.replace("os.path.dirname(os.path.realpath(__file__))", "\"" + projectfiles + "\"")
## WRITE the new file
with open(project_pyfile, "w") as pf:
    pf.write(newcontents)

# change data/project.json contents
## READ project.json
data_file = os.path.join(project_directory, "data", "project.json")
with open(data_file, "r") as tdf:
    templatedatacontents = tdf.read()
os.remove(data_file)
## REPLACE newproj with the new project name
newdatacontents = templatedatacontents.replace("newproj", project_name)
## WRITE the new file
with open(data_file, "w") as tdf2:
    tdf2.write(newdatacontents)

print("""Use the command:
python3 %s
To serve the project at url localhost:8000
and localhost:8000/skiadmin for the admin pages""" % (project_pyfile,))
sys.exit(0)


