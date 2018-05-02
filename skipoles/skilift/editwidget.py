####### SKIPOLE WEB FRAMEWORK #######
#
# editwidget.py of skilift package  - functions for editing a widget
#
# This file is part of the Skipole web framework
#
# Date : 20180403
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2018 Bernard Czenkusz
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


"""Functions for editing a widget"""

import pkgutil


from ..ski import skiboot, widgets
from ..ski.excepts import ServerError

from . import project_loaded, widget_info


def widget_modules():
    "Return a tuple of widget modules"
    return tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(widgets.__path__))



