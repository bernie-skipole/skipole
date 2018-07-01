####### SKIPOLE WEB FRAMEWORK #######
#
# editvalidator.py of skilift package  - functions for editing a validator
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


"""Functions for editing a validator"""

import pkgutil, re, importlib, inspect


from ..ski import skiboot, validators
from ..ski.excepts import ServerError

from . import get_proj_page

from .info_tuple import ResponderInfo


# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w]')


def validator_names():
    "Returns a tuple of validator names"
    return tuple(name for (module_loader, name, ispkg) in pkgutil.iter_modules(validators.__path__))




