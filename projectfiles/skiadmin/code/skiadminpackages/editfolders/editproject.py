####### SKIPOLE WEB FRAMEWORK #######
#
# editproject.py  - get and put functions for the edit project page
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


import os

from skipole import skilift
from skipole import FailPage, ValidateError, ServerError



def retrieve_about_skilift(skicall):
    "About skilift page"
    skicall.page_data[("adminhead","page_head","large_text")] = "skilift"


def get_text(skicall):
    """Finds any widget submitting 'get_field' with value of a textblock ref, returns
       page_data with key widget with field 'div_content' and value the textblock text"""

    page_data = skicall.page_data

    if 'received' not in skicall.submit_dict:
        return
    received_widgfields = skicall.submit_dict['received']
    for key, val in received_widgfields.items():
        if isinstance(key, tuple) and (key[-1] == 'get_field'):
            text = skicall.textblock(val)
            if text is None:
                continue
            text = text.replace('\n', '\n<br />')
            if len(key) == 3:
                page_data[(key[0], key[1],'div_content')] = text
                page_data[(key[0], key[1],'hide')] = False
            elif len(key) == 2:
                page_data[(key[0],'div_content')] = text
                page_data[(key[0],'hide')] = False

