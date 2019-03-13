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

import os, tarfile, shutil, tempfile

from .ski import skiboot, read_json

# need to import projectcode, as importing it runs "skiboot.set_projectcode(os.path.dirname(os.path.realpath(__file__)))"
# so skiboot then knows the location of the project code directory

from . import projectcode

from .ski.project_class_definition import Project

from .ski.excepts import ServerError

version = skiboot.version()
adminproj = skiboot.admin_project()
newproj = skiboot.new_project()
libproj = skiboot.lib_project()


class WSGIApplication(Project):
    "This class has a __call__ method which makes it a wsgi application"

    def __init__(self, project, options={}, projectfiles=None):
        "Creates the top root project"
        if projectfiles:
            # sets the location of projectfiles into skiboot
            skiboot.set_projectfiles(projectfiles)
        Project.__init__(self, project, options=options, rootproject=True)
        # set this project as the site root project
        skiboot.set_site_root(self)
        # Call the start_project functions for this project and any sub_projects
        self.start_project()

    def __call__(self, environ, start_response):
        "Defines this projects callable as the wsgi application"
        status, headers, data = self.respond(environ)
        start_response(status, headers)
        return data


def set_projectfiles(projectfiles):
    "Set the directory where where project data is stored"
    skiboot.set_projectfiles(projectfiles)


def get_projectfiles():
    "Get the directory where where project data is stored"
    return skiboot.projectfiles()


def set_debug(mode):
    "If mode is True, this sets increased debug error messages to be displayed"
    skiboot.set_debug(mode)


def load_project(proj_ident, options={}, projectfiles=None):
    """Returns a Project instance"""
    if projectfiles:
        # sets the location of projectfiles into skiboot
        skiboot.set_projectfiles(projectfiles)
    # create a Project instance
    return Project(proj_ident, options=options)



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


def remove_project(proj_ident):
    "Removes the project by deleting symlinks"

    if proj_ident == adminproj:
        raise ServerError(message = "Cannot remove the admin project %s" % (adminproj,))

    if proj_ident == newproj:
        raise ServerError(message = "Cannot remove %s, this is used to generate new projects." % (newproj,))

    if proj_ident == libproj:
        raise ServerError(message = "Cannot remove %s, this is used to provide static libraries." % (libproj,))

    project_dir = skiboot.projectpath(proj_ident)
    code_dir = skiboot.projectcode(proj_ident)

    if not ( os.path.isdir(project_dir) or os.path.islink(project_dir) or os.path.isdir(code_dir) or os.path.islink(code_dir)):
        # project directories not found
        raise ServerError(message = "This project has not been found")

    print("This operation removes project %s by deleting symlinks." % (proj_ident,))
    print("Please confirm you wish to do this.")
    responce = input('Type Yes to proceed :')
    if responce == 'Yes':
        print("Removing project symlinks...")
    else:
        print("Project not removed.")
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
        except Exception:
            print("Error while attempting to remove %s" % (project_dir,))
        else:
            print("Removed Symlink: %s" % (project_dir,))
            projecfiles_deleted = True
    else:
        print("Symlink %s not found" % (project_dir,))

    # delete project code directory
    if os.path.isdir(code_dir) or os.path.islink(code_dir):
        try:
            if os.path.islink(code_dir):
                os.unlink(code_dir)
            else:
                shutil.rmtree(code_dir)
        except Exception:
            print("Error while attempting to remove %s" % (code_dir,))
        else:
            print("Removed Symlink: %s" % (code_dir,))
            projectcode_deleted = True
    else:
        print("Symlink %s not found" % (code_dir,))

    if projecfiles_deleted and projectcode_deleted:
        print("Project Removed.")
    elif projecfiles_deleted:
        print("Project files symlink deleted, however the project code symlink was not!")
    elif projectcode_deleted:
        print("Project code symlink deleted, however the project files symlink was not!")
    else:
        raise ServerError(message = "Error: Unable to delete symlinks")


def copy_proj(symlinkdir, source_id, project):
    "Creates a new project by copying source_id to project, and by changing filepaths"
    #  check the project name given
    if not project:
        raise ServerError(message = "Error - a project name must be given")
    if not (project.isalnum() and project.islower()):
        raise ServerError(message = "Error - the project name must be lower case alphanumeric only")
    if project.isdigit():
        raise ServerError(message = "Error - the project name must have some letters")
    if source_id == project:
        raise ServerError(message = "Error - cannot copy to itself")
    if project == 'skiadmin':
        raise ServerError(message = "Error - skiadmin is a reserved name")
    if project == skiboot.admin_project():
        raise ServerError(message = "Error - Sorry, this is a reserved name")

    project_dir =  skiboot.projectpath(proj_ident=project)
    if os.path.isdir(project_dir):
        raise ServerError(message = "Error - project directory already exists")

    source_proj_dir =  skiboot.projectpath(proj_ident=source_id)
    if not os.path.isdir(source_proj_dir):
        raise ServerError(message = "Error - project to be copied cannot be found")

    if not os.path.isdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s not found." % (symlinkdir,))
    if os.listdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s has contents." % (symlinkdir,))

    # the projectfiles and projectcode directories
    symprojectfiles = os.path.join(symlinkdir, 'projectfiles')
    symprojectcode = os.path.join(symlinkdir, 'projectcode')

    try:

        # copy files to symprojectfiles/data, symprojectfiles/static and symprojectcode

        os.mkdir(symprojectfiles)

        source = skiboot.projectstatic(source_id)
        destination = os.path.join(symprojectfiles, 'static')
        shutil.copytree(source, destination)

        source = skiboot.projectdata(source_id)
        destination = os.path.join(symprojectfiles, 'data')
        shutil.copytree(source, destination)

        projectjson = os.path.join(destination, "project.json")

        # in project.json swap out
        # "filepath": "source_id
        # for
        # "filepath": "project
 
        current_loc = "\"filepath\": \"%s" % source_id
        new_loc = "\"filepath\": \"%s" % project
        with open(projectjson, 'r') as f:
            read_data = f.read()
        new_data = read_data.replace(current_loc, new_loc)
        with open(projectjson, 'w') as f:
            f.write(new_data)

        # copy code
        source = skiboot.projectcode(source_id)
        shutil.copytree(source, symprojectcode, ignore=shutil.ignore_patterns('*.pyc'))
    except Exception:
        raise ServerError(message = "Error - An unknown error occurred, partial files may have been created and may need cleaning up")

    # create symlinks
    os.symlink(symprojectfiles, project_dir)
    code_dir = skiboot.projectcode(project)
    os.symlink(symprojectcode, code_dir)



def copy_newproj_to_symlink(symlinkdir, project):
    "Get newproj, then copy and symlink it"
    # first, check symlinkdir
    if not os.path.isdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s not found." % (symlinkdir,))
    if os.listdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s has contents." % (symlinkdir,))
    # get the 'newproj' name
    source_id = skiboot.new_project()
    if source_id == project:
        raise ServerError(message = "Error - %s is a reserved name" % (source_id,))
    # copy project
    copy_proj(symlinkdir, source_id, project)


def copy_proj_to_symlink(symlinkdir, source_id, project):
    "Copy project and symlink it"
    # first, check symlinkdir
    if not os.path.isdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s not found." % (symlinkdir,))
    if os.listdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s has contents." % (symlinkdir,))
    # Now do copy
    copy_proj(symlinkdir, source_id, project)


def import_project(symlinkdir, tarfilepath):
    "Import project tar file, then symlink it, returns the project name"
    # first, check symlinkdir
    if not os.path.isdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s not found." % (symlinkdir,))
    if os.listdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s has contents." % (symlinkdir,))
    # check tarfilepath
    if not os.path.isfile(tarfilepath):
        raise ServerError(message = "Error - File %s not found." % (tarfilepath,))
    if not tarfile.is_tarfile(tarfilepath):
        raise ServerError(message = "Error - File %s is not a tar file." % (tarfilepath,))
    with tarfile.open(tarfilepath, "r") as tar:
        # first item should be proj_ident/xxxxx, such as proj_ident/myapp.py or proj_ident/__main__.py
        firstitem = tar.getnames()[0]
    proj_file = firstitem.split('/')
    if len(proj_file) != 2:
        proj_file = firstitem.split('\\')
    if len(proj_file) != 2:
        raise ServerError(message = "Error - Cannot parse contents of file %s" % (tarfilepath,))

    project = proj_file[0]

    # check project_dir does not already exist
    project_dir = skiboot.projectpath(project)
    if os.path.isdir(project_dir):
        raise ServerError(message = "Error - Project %s found in the file already exists." % (project,))

    # make project directory and copy tar file to it
    tarpath = os.path.join(symlinkdir, project + ".tar.gz")
    shutil.copyfile(tarfilepath, tarpath)

    # the projectfiles and projectcode directories
    symprojectfiles = os.path.join(symlinkdir, 'projectfiles')
    symprojectcode = os.path.join(symlinkdir, 'projectcode')

    # and build the project
    try:
        print("Extracting tar file...")

        # create a temporary directory in which to do the extraction
        with tempfile.TemporaryDirectory() as exportdir:
            # do the extraction to export directory
            with tarfile.open(tarpath, "r") as tar:
                tar.extractall(path=exportdir, members = _get_files(tar, project))
 
            # copy files from export directory to symprojectfiles/data, symprojectfiles/static and symprojectcode

            os.mkdir(symprojectfiles)

            source = os.path.join(exportdir, project, 'projectfiles', project, 'data')
            destination = os.path.join(symprojectfiles, 'data')
            shutil.copytree(source, destination)

            source = os.path.join(exportdir, project, 'projectfiles', project, 'static')
            destination = os.path.join(symprojectfiles, 'static')
            shutil.copytree(source, destination)

            source = os.path.join(exportdir, project, 'skipoles', 'projectcode', project)
            shutil.copytree(source, symprojectcode)

    except Exception:
        raise ServerError(message = "Error during import")

    # create symlinks
    os.symlink(symprojectfiles, project_dir)
    code_dir = skiboot.projectcode(project)
    os.symlink(symprojectcode, code_dir)
    # check project.json can be read, and is of an acceptable version
    try:
        read_json.read_project(project)
    except Exception:
        os.unlink(project_dir)
        os.unlink(code_dir)
        raise
    return project



def make_symlink_to_project(symlinkdir, project):
    "Makes symlinks from symlink directory to project files"
    if not os.path.isdir(symlinkdir):
        raise ServerError(message = "Error - Directory %s not found." % (symlinkdir,))
    symprojectfiles = os.path.join(symlinkdir, 'projectfiles')
    if not os.path.exists(symprojectfiles):
        raise ServerError(message = "Error - Directory %s not found." % (symprojectfiles,))
    symprojectcode = os.path.join(symlinkdir, 'projectcode')
    if not os.path.exists(symprojectcode):
        raise ServerError(message = "Error - Directory %s not found." % (symprojectcode,))
    project_dir = skiboot.projectpath(project)
    code_dir = skiboot.projectcode(project)
    if os.path.isdir(project_dir) or os.path.isdir(code_dir):
        # project directories already exist
        raise ServerError(message = "Error - Project directories already exist.")
    # create symlinks
    os.symlink(symprojectfiles, project_dir)
    os.symlink(symprojectcode, code_dir)
    # check project.json can be read, and is of an acceptable version
    try:
        read_json.read_project(project)
    except Exception:
        os.unlink(project_dir)
        os.unlink(code_dir)
        raise


