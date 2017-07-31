####### SKIPOLE WEB FRAMEWORK #######
#
# __init__.py  - The Skipole web site builder
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

import os, tarfile, shutil, sys, tempfile

from .ski import skiboot, project_class_definition

from .ski.excepts import ServerError

version = skiboot.version()
adminproj = skiboot.admin_project()
newproj = skiboot.new_project()
libproj = skiboot.lib_project()

# set the path of the projectfiles directory where project data is stored
projectfiles = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'projectfiles')

# Set the directory where project files can be found"
skiboot.set_projectfiles(projectfiles)


def set_debug(mode):
    "If mode is True, this sets increased debug error messages to be displayed"
    skiboot.set_debug(mode)


def load_project(proj_ident, options={}, rootproject = True):
    """Load a rootproject, then loads any sub projects.
       Returns the project.  If project not found, returns None"""

    # get project location
    project_dir = skiboot.projectpath(proj_ident)
    if not os.path.isdir(project_dir):
        return

    # create a Project instance
    project = project_class_definition.Project(proj_ident)
    # load project from json files
    project.load_from_json(rootproject)

    # set this project as the main site project
    if rootproject:
        skiboot.set_site_root(project)

    if options:
        if proj_ident in options:
            project.option = options[proj_ident]
        if rootproject:
            # If this is a root project, then set any subproject options
            for subproj_ident in options:
                if subproj_ident != proj_ident:
                    project.set_subproject_option(projectname, options[subproj_ident])

    if rootproject:
        # Call the start_project function for this project and any sub_projects
        project.start_project()

    return project


def _get_files(members, proj_ident):
    "Generator yielding tarinfo members"

    # extract data directory
    tar_data_dir = os.path.join(proj_ident, 'projectfiles', proj_ident, 'data')
    tar_data_dir += os.sep

    # extract static directory
    tar_static_dir = os.path.join(proj_ident, 'projectfiles', proj_ident, 'static')
    tar_static_dir += os.sep

    # extract code
    tar_code_dir = os.path.join(proj_ident, 'skipoles', 'projectcode', proj_ident)
    tar_code_dir += os.sep

    for tarinfo in members:
        # extract data directory
        if tarinfo.name.startswith(tar_data_dir):
            yield tarinfo
        # extract static directory
        elif tarinfo.name.startswith(tar_static_dir):
            yield tarinfo
        # extract code
        elif tarinfo.name.startswith(tar_code_dir):
            yield tarinfo


def delete_project(proj_ident):
    "Deletes the project"

    if proj_ident == adminproj:
        print("Cannot delete the admin project %s" % (adminproj,))
        return

    if proj_ident == newproj:
        print("Cannot delete %s, this is used to generate new projects." % (newproj,))
        return

    if proj_ident == libproj:
        print("Cannot delete %s, this is used to provide static libraries." % (libproj,))
        return

    project_dir = skiboot.projectpath(proj_ident)
    code_dir = skiboot.projectcode(proj_ident)

    if not ( os.path.isdir(project_dir) or os.path.islink(project_dir) or os.path.isdir(code_dir) or os.path.islink(code_dir)):
        # project directories not found
        print("This project has not been found")
        return

    print("This operation deletes project %s" % (proj_ident,))
    print("Are you sure you wish to do this?")
    responce = input('Type Yes to proceed :')
    if responce == 'Yes':
        print("Deleting project...")
    else:
        print("Project not deleted. Command terminated.")
        return

    projecfiles_deleted = False
    projectcode_deleted = False

    # delete project files directory
    if os.path.isdir(project_dir) or os.path.islink(project_dir):
        try:
            if os.path.islink(project_dir):
                os.unlink(project_dir)
            else:
                shutil.rmtree(project_dir)
        except:
            print("Error while attempting to delete %s" % (project_dir,))
        else:
            print("Deleted: %s" % (project_dir,))
            projecfiles_deleted = True
    else:
        print("Directory %s not found" % (project_dir,))

    # delete project code directory
    if os.path.isdir(code_dir) or os.path.islink(code_dir):
        try:
            if os.path.islink(code_dir):
                os.unlink(code_dir)
            else:
                shutil.rmtree(code_dir)
        except:
            print("Error while attempting to delete %s" % (code_dir,))
        else:
            print("Deleted: %s" % (code_dir,))
            projectcode_deleted = True
    else:
        print("Directory %s not found" % (code_dir,))

    if projecfiles_deleted and projectcode_deleted:
        print("Project deleted.")
    elif projecfiles_deleted:
        print("Project files directory deleted, however the project code directory was not deleted")
    elif projectcode_deleted:
        print("Project code directory deleted, however the project files directory was not deleted")
    else:
        print("Unable to delete directories")


def copy_newproj_to(project):
    "Creates a new project by copying newproj to project, and by changing filepaths"
    # get the 'newproj' name
    source_id = skiboot.new_project()
    if source_id == project:
        print("Error - %s is a reserved name" % (source_id,))
        sys.exit(8)
    # copy project
    copy_proj(source_id, project)


def copy_proj(source_id, project):
    "Creates a new project by copying source_id to project, and by changing filepaths"
    #  check the project name given
    if not project:
        print("Error - a project name must be given")
        sys.exit(8)
    if not (project.isalnum() and project.islower()):
        print("Error - the project name must be lower case alphanumeric only")
        sys.exit(8)
    if project.isdigit():
        print("Error - the project name must have some letters")
        sys.exit(8)
    if source_id == project:
        print("Error - cannot copy to itself")
        sys.exit(8)
    if project == 'skiadmin':
        print("Error - skiadmin is a reserved name")
        sys.exit(8)
    if project == skiboot.admin_project():
        print("Error - Sorry, this is a reserved name")
        sys.exit(8)

    proj_dir =  skiboot.projectpath(proj_ident=project)
    if os.path.isdir(proj_dir):
        print("Error - project directory already exists")
        sys.exit(8)
    source_proj_dir =  skiboot.projectpath(proj_ident=source_id)
    if not os.path.isdir(source_proj_dir):
        print("Error - project to be copied cannot be found")
        sys.exit(8)
    try:
        # create directory structure
        os.mkdir(proj_dir)
        # copy static directory and contents
        newproject_static = skiboot.projectstatic(project)
        source_project_static = skiboot.projectstatic(source_id)
        shutil.copytree(source_project_static, newproject_static)
        # copy data directory and contents
        newproject_data = skiboot.projectdata(project)
        source_project_data = skiboot.projectdata(source_id)
        shutil.copytree(source_project_data, newproject_data)

        # get project.json and swap out
        # "filepath": "source_id
        # for
        # "filepath": "project
        # where it occurs in the project.json file
        newproject_json = skiboot.project_json(project)
        current_loc = "\"filepath\": \"%s" % source_id
        new_loc = "\"filepath\": \"%s" % project
        with open(newproject_json, 'r') as f:
            read_data = f.read()
        new_data = read_data.replace(current_loc, new_loc)
        with open(newproject_json, 'w') as f:
            f.write(new_data)

        # copy code
        source_project_code = skiboot.projectcode(source_id)
        newproject_code = skiboot.projectcode(project)
        shutil.copytree(source_project_code, newproject_code, ignore=shutil.ignore_patterns('*.pyc'))
    except:
        print("Error - An unknown error occurred, partial files may have been created and may need cleaning up")
        sys.exit(8)


def copy_newproj_to_symlink(symlinkdir, project):
    "Create new project, then copy and symlink it"
    # first, check symlinkdir
    if not os.path.isdir(symlinkdir):
        print("Error - Directory %s not found." % (symlinkdir,))
        sys.exit(8)
    if os.listdir(symlinkdir):
        print("Error - Directory %s has contents." % (symlinkdir,))
        sys.exit(8)
    # Now do new project creation
    copy_newproj_to(project)
    # Now copy and symlink
    make_symlink_from_project(symlinkdir, project)


def copy_proj_to_symlink(symlinkdir, source_id, project):
    "Copy project and symlink it"
    # first, check symlinkdir
    if not os.path.isdir(symlinkdir):
        print("Error - Directory %s not found." % (symlinkdir,))
        sys.exit(8)
    if os.listdir(symlinkdir):
        print("Error - Directory %s has contents." % (symlinkdir,))
        sys.exit(8)
    # Now do copy
    copy_proj(source_id, project)
    # and symlink
    make_symlink_from_project(symlinkdir, project)


def import_project(tarfilepath):
    "imports a project tar file"
    if not os.path.isfile(tarfilepath):
        print("Error - File %s not found." % (tarfilepath,))
        sys.exit(8)

    if not tarfile.is_tarfile(tarfilepath):
        print("Error - File %s is not a tar file." % (tarfilepath,))
        sys.exit(8)

    with tarfile.open(tarfilepath, "r") as tar:
        # first item should be proj_ident/__main__.py
        pyfile = tar.getnames()[0]

    proj_main = pyfile.split('/')
    if len(proj_main) != 2:
        proj_main = pyfile.split('\\')
    if len(proj_main) != 2:
        print("Error - Cannot parse contents of file %s" % (tarfilepath,))
        sys.exit(8)

    main_name = proj_main[1]
    if main_name != '__main__.py':
        print("Error - Cannot parse contents of file %s" % (tarfilepath,))
        sys.exit(8)

    project = proj_main[0]

    # get project location, if project dir exits, return
    project_dir = skiboot.projectpath(project)
    if os.path.isdir(project_dir):
        print("Error - Project %s found in the file already exists." % (project,))
        sys.exit(8)

    # make project directory and copy tar file to it
    os.mkdir(project_dir)
    tarpath = skiboot.tar_path(project)
    shutil.copyfile(tarfilepath, tarpath)

    # and build the project
    try:
        print("Extracting tar file...")

        # create a temporary directory in which to do the extraction
        with tempfile.TemporaryDirectory() as exportdir:
            # do the extraction to export directory
            with tarfile.open(tarpath, "r") as tar:
                tar.extractall(path=exportdir, members = _get_files(tar, project))

            # copy files from export directory to the right places

            # delete data directory and copy from export directory
            destination = skiboot.projectdata(project)
            if os.path.isdir(destination):
                shutil.rmtree(destination)
            source = os.path.join(exportdir, project, 'projectfiles', project, 'data')
            shutil.copytree(source, destination)

            # delete static directory and copy from export directory
            destination = skiboot.projectstatic(project)
            if os.path.isdir(destination):
                shutil.rmtree(destination)
            source = os.path.join(exportdir, project, 'projectfiles', project, 'static')
            shutil.copytree(source, destination)

            # delete project code directory and copy from export directory
            source = os.path.join(exportdir, project, 'skipoles', 'projectcode', project)
            destination = skiboot.projectcode(project)
            if os.path.isdir(destination):
                if os.path.islink(destination):
                    real_destination = os.path.realpath(destination)
                    os.unlink(destination)
                    shutil.rmtree(real_destination)
                    shutil.copytree(source, real_destination)
                    os.symlink(real_destination, destination)
                else:
                    shutil.rmtree(destination)
                    shutil.copytree(source, destination)

    except ServerError as e:
        print(e.message)
        print("Clearing out project files")
        # clear out any files
        cleared = True
        if os.path.isdir(project_dir):
            try:
                if os.path.islink(project_dir):
                    os.unlink(project_dir)
                else:
                    shutil.rmtree(project_dir)
            except:
                print("Error while attempting to delete %s" % (project_dir,))
                cleared = False
        code_dir = skiboot.projectcode(project)
        if os.path.isdir(code_dir):
            try:
                if os.path.islink(code_dir):
                    os.unlink(code_dir)
                else:
                    shutil.rmtree(code_dir)
            except:
                print("Error while attempting to delete %s" % (code_dir,))
                cleared = False
        if cleared:
            print("Import failed")
        else:
            print("Import failed but invalid data may remain under projectfiles and projectcode directories")
        sys.exit(8)

    print("Project imported; run 'skipole.py -a %s' to administer the project." % (project,))



def make_symlink_from_project(symlinkdir, project):
    "Copies project files to symlink directory"
    project_dir = skiboot.projectpath(project)
    code_dir = skiboot.projectcode(project)
    if (not os.path.isdir(project_dir)) and (not os.path.isdir(code_dir)):
        # project directories not found
        print("Error - This project has not been found")
        sys.exit(8)
    if not os.path.isdir(symlinkdir):
        print("Error - Directory %s not found." % (symlinkdir,))
        sys.exit(8)
    if os.listdir(symlinkdir):
        print("Error - Directory %s has contents." % (symlinkdir,))
        sys.exit(8)
    symprojectfiles = os.path.join(symlinkdir, 'projectfiles')
    symprojectcode = os.path.join(symlinkdir, 'projectcode')
    # copy contents of project_dir to symprojectfiles
    shutil.copytree(project_dir, symprojectfiles)
    # copy contents of code_dir to symprojectcode
    shutil.copytree(code_dir, symprojectcode)
    # remove old directories
    shutil.rmtree(project_dir)
    shutil.rmtree(code_dir)
    # and create symlinks
    make_symlink_to_project(symlinkdir, project)


def make_symlink_to_project(symlinkdir, project):
    "Makes symlinks from symlink directory to project files"
    if not os.path.isdir(symlinkdir):
        print("Error - Directory %s not found." % (symlinkdir,))
        sys.exit(8)
    symprojectfiles = os.path.join(symlinkdir, 'projectfiles')
    if not os.path.exists(symprojectfiles):
        print("Error - Directory %s not found." % (symprojectfiles,))
        sys.exit(8)
    symprojectcode = os.path.join(symlinkdir, 'projectcode')
    if not os.path.exists(symprojectcode):
        print("Error - Directory %s not found." % (symprojectcode,))
        sys.exit(8)
    project_dir = skiboot.projectpath(project)
    code_dir = skiboot.projectcode(project)
    if os.path.isdir(project_dir) or os.path.isdir(code_dir):
        # project directories already exist
        print("Error -Project directories already exist.")
        sys.exit(8)
    # create symlinks
    os.symlink(symprojectfiles, project_dir)
    os.symlink(symprojectcode, code_dir)


