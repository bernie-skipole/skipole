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

import pkgutil, importlib, inspect

from collections import namedtuple


from ..ski import skiboot, widgets
from ..ski.excepts import ServerError

from . import project_loaded, widget_info

WidgetDescription = namedtuple('Widget', ['classname', 'reference', 'fields', 'containers', 'illustration'])

# 'fields' is a list of lists: [ field arg, field ref]
# 'containers' is the number of containers in the widget, 0 for none

def widget_modules():
    "Return a tuple of widget module names"
    return tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(widgets.__path__))


def widgets_in_module(module_name):
    "Returns a list of WidgetDescription's present in the module"
    module = importlib.import_module("skipoles.ski.widgets." + module_name)
    widget_list = []
    for classname,obj in inspect.getmembers(module, lambda member: inspect.isclass(member) and (member.__module__ == module.__name__)):
        widget_list.append( WidgetDescription( classname,
                                               obj.description_ref(),
                                               obj.arg_references(),
                                               obj.len_containers(),
                                               obj.description()
                                               ) )
    return widget_list

        



