#
# This script is meant to be run from the command line using
#
# python3 -m skipole mynewproj /path/to/projectfiles
#


import sys, os, re, shutil

from . import version

DESCRIPTION = """Usage is

python3 -m skipole mynewproj /path/to/projectfiles

Which creates a directory /path/to/projectfiles
containing three sub directories:

mynewproj - a subdirectory containing a new project
skis - a project serving needed javascript files, necessary for all projects
skiadmin - a project used to help develop 'mynewproj'

You should replace 'mynewproj' with your preferred name for a new project.
This is an optional argument. If not given then only the skis and skiadmin
projects will be created.

The path "/path/to/projectfiles" must be given, and is the path to a directory
where you will develop your project. Multiple projects can be created in one
'projectfiles' directory, or you could have multiple such directories holding
different projects.

If the directory already exists, any existing skiadmin and skis projects will
be overwritten, this facility is used to upgrade skis and skiadmin if a new
version of skipole is installed.

If mynewproj already exists in the directory, it will not be changed.
"""


# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')




if __name__ == "__main__":
    # do the work
    print("Skipole version: %s" % (version,))
    args = sys.argv
    
    if len(args) == 3:
        project_name = args[1]
        projectfiles = args[2]
        if _AN.search(project_name):
            print( "Error: Invalid project name, alphanumeric or underscore only")
            sys.exit(1)
        if (project_name == 'skis') or (project_name=='skiadmin'):
            print("Error: This project name is reserved")
            sys.exit(1)
    elif len(args) == 2:
        project_name = None
        projectfiles = args[1]
    else:
        print( "Invalid input. " + DESCRIPTION)
        sys.exit(1)

    # get the location of the template directory which is to be copied
    template_directory = os.path.join(os.path.dirname(os.path.dirname(args[0])), 'projectfiles')
    if not os.path.isdir(template_directory):
        print("Error: Cannot find the template data for the skis and skiadmin projects")
        sys.exit(1)

    # Does the given directory exist
    if not os.path.isdir(projectfiles):
        # directory does not exist, create it by copying the template_directory
        shutil.copytree(template_directory, projectfiles)
        template_newproj_directory = os.path.join(projectfiles, 'newproj')
        if project_name is None:
            # remove the template new project
            shutil.rmtree(template_newproj_directory)
            print("Project directory %s created" % (projectfiles,))
            sys.exit(0)
        # A project name is given,
        new_code_path = os.path.join(projectfiles, project_name, "code", project_name + ".py")
        print("Creating %s" % (new_code_path,))
        # change newproj.py to project_name.py, including the contents
        template_newproj_file = os.path.join(template_newproj_directory, "code", "newproj.py")
        with open(template_newproj_file, "r") as tnf:
            templatecontents = tnf.read()
        os.remove(template_newproj_file)
        newcontents = templatecontents.replace("newproj", project_name)
        project_file = os.path.join(template_newproj_directory, "code", project_name + ".py")
        with open(project_file, "w") as pf:
            pf.write(newcontents)

        # change data/project.json contents
        template_data_file = os.path.join(template_newproj_directory, "data", "project.json")
        with open(template_data_file, "r") as tdf:
            templatedatacontents = tdf.read()
        os.remove(template_data_file)
        newdatacontents = templatedatacontents.replace("newproj", project_name)
        with open(template_data_file, "w") as tdf2:
            tdf2.write(newdatacontents)
        # and change the name of the template_newproj_directory to project_name
        os.rename(template_newproj_directory, os.path.join(projectfiles, project_name))
        print("Project directory %s created, with new project %s" % (projectfiles,project_name))
        print("""Use the command:
python3 %s
To serve the project at url localhost:8000
and localhost:8000/skiadmin for the admin pages""" % (new_code_path,))
        sys.exit(0)
        



