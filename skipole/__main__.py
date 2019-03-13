#
# this script is meant to be run from the command line using
#
# python3 -m skipole /path/to/projectfiles
#
# where /path/to/projectfiles is the path to a project directory
#
# If the directory does not exist it will be created, together
# with skiadmin, skis and newproject directories and contents
#
# If it exists the presence of skiadmin, skis and newproject
# will be checked. If they do not exist they will be created
#
# If they do exist they will be copied to
# skiadmin_old, skis_old and newproject_old
# and new skiadmin, skis and newproject directories and contents
# will be created
# 

import sys

from . import version


if __name__ == "__main__":
    # do the work
    print(version)
    print(sys.argv)
