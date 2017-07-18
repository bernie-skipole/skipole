###### SKIPOLE WEB FRAMEWORK #######
#
# package editfiles
#
# This file is part of the Skipole web framework
#
# Date : 20170221
#
# Author : Bernard Czenkusz
# Email  : bernie@skipole.co.uk
#
#
#   Copyright 2017 Bernard Czenkusz
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


from . import editfile
from ....ski.excepts import FailPage



def submit_data(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Depending on the submit list, call the appropriate package function"

    # submit_list[0] is the string 'editfiles' and has already been used to call this fuction
    assert submit_list[0] == 'editfiles'

    if submit_list[1] == 'editfile':
        try:
            submitfunc = getattr(editfile, submit_list[2])
        except:
            raise FailPage("submit_list contains 'editfiles', 'editfile', but the required function is not recognised")
        return submitfunc(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang)

    raise FailPage("submit_list module string %s not recognised" % (submit_list[1],))
