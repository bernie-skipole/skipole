####### SKIPOLE WEB FRAMEWORK #######
#
# editresponder.py of skilift package  - functions for editing a responder
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


"""Functions for editing a responder"""

import inspect

from collections import namedtuple

from ..ski import skiboot, responders
from ..ski.excepts import ServerError

from . import project_loaded


ResponderInfo = namedtuple('ResponderInfo', ['responder', 'description_ref'])
# responder is the class name of the responder
# description_ref is the TextBlock reference describing the responder


def list_responders():
    """Returns a list of ResponderInfo tuples"""
    responderlist = []
    for name,item in inspect.getmembers(responders, inspect.isclass):
        if issubclass(item, responders.Respond):
            if name == 'Respond': continue
            responderlist.append(ResponderInfo(name, item.description_ref()))
    return responderlist




