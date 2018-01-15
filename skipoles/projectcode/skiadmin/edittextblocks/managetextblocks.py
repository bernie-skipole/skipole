####### SKIPOLE WEB FRAMEWORK #######
#
# managetextblocks.py  - for managing and editing textblocks
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

import re

# a search for anything none-alphanumeric and not an underscore
_TB = re.compile('[^\w\.]')

from ....ski.excepts import FailPage
from .... import skilift


def retrieve_link_table(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the manage textblocks page"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    page_data[("adminhead","page_head","large_text")] = "Manage TextBlocks"

    accesstextblocks = skilift.get_accesstextblocks(proj_ident)

    result = accesstextblocks.get_textrefs()
    # result is a list of textrefs

    #       contents: col 0 is the text to place in the first column,
    #                  col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
    #                  col 5 - True if the first button and link is to be shown, False if not
    #                  col 6 - True if the second button and link is to be shown, False if not
    #                  col 7 - True if the third button and link is to be shown, False if not
    #                  col 8 - True if the fourth button and link is to be shown, False if not

    page_data[('txtblocks', 'contents')] = [ [ref, ref, ref, '', '', True, True, False, False] for ref in result if '.' not in ref]
    if not page_data[('txtblocks', 'contents')]:
        page_data[('txtblocks', 'show')] = False
    else:
        page_data[('txtblocks', 'contents')].sort(key=lambda r: r[0])

    # set page data for widget tables000.Table1_Button name moretblocks - displaying refs that do have a '.' in them
    # contents: col 0 is the text to place in the first column, col 1 is the get field

    reflinklist = []
    for ref in result:
        if '.' not in ref:
            continue
        ritem = ref.split('.')[0]
        if ritem not in reflinklist:
            reflinklist.append(ritem)


    if not reflinklist:
        page_data[('moretblocks', 'show')] = False
        return
    
    page_data[('moretblocks', 'contents')] = [ [ref + "...", ref] for ref in reflinklist]
    page_data[('moretblocks', 'contents')].sort(key=lambda r: r[0])


def retrieve_more(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for further textblock tables"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    page_data[("adminhead","page_head","large_text")] = "Further TextBlocks"
    call_data['extend_nav_buttons'] = []

    reference = call_data['ref']
    reflist = reference.split('.')
    refdot = reference + '.'

    # a back button is added if ref has a . in it
    if '.' in reference:
        backref = '.'.join(reflist[:-1])
        call_data['extend_nav_buttons'].append([4006, "Previous", True, backref])

    # set input text
    page_data[("st1","input_text")] = refdot

    # list of textrefs
    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    result = accesstextblocks.get_textrefs()              

    # set result to a list of textrefs that start with refdot
    result = [ ref for ref in result if ref.startswith(refdot) ]

    if not result:
        raise FailPage("No further references found")

   #       contents: col 0 is the text to place in the first column,
    #                  col 1, 2, 3, 4 are the get field contents of links 1,2,3 and 4
    #                  col 5 - True if the first button and link is to be shown, False if not
    #                  col 6 - True if the second button and link is to be shown, False if not
    #                  col 7 - True if the third button and link is to be shown, False if not
    #                  col 8 - True if the fourth button and link is to be shown, False if not


    displaylen = len(reflist) + 1

    newresult = [ ref for ref in result if displaylen == len(ref.split('.')) ]

    if newresult:
        page_data[('txtblocks', 'contents')] = [ [ref, ref,  ref, '', '',  True, True, False, False] for ref in newresult]
        page_data[('txtblocks', 'contents')].sort(key=lambda r: r[0])
    else:
        page_data[('txtblocks', 'show')] = False

    # The more table displays remaining refs in result

    # set page data for widget tables000.Table1_Button name moretblocks - displaying remaining refs
    # contents: col 0 is the text to place in the first column, col 1 is the get_field
 
    reflinklist = []
    for ref in result:
        if ref in newresult:
            continue
        rlist = ref.split('.')
        ritem = '.'.join(rlist[:displaylen])
        if ritem not in reflinklist:
            reflinklist.append(ritem)

    if not reflinklist:
        page_data[('moretblocks', 'show')] = False
        return
    
    page_data[('moretblocks', 'contents')] = [ [ref + "...", ref] for ref in reflinklist]
    page_data[('moretblocks', 'contents')].sort(key=lambda r: r[0])


def retrieve_textblock(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Gets data for the edit textblock page"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident
    language = lang[0].lower()
    default_language = lang[1]

    page_data[("adminhead","page_head","large_text")] = "Edit TextBlock"
    call_data['extend_nav_buttons'] = []

    if 'textblock' in call_data:
        edited_textblock = call_data['textblock']
    else:
        raise FailPage("TextBlock Reference not found")

    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    result = accesstextblocks.get_textref_languages()
    # result is a dictionary {textref: [languages],...}
    if not edited_textblock in result:
        raise FailPage("The TextBlock reference has not been found")

    if '.' in edited_textblock:
        reflist = edited_textblock.split('.')
        backref = '.'.join(reflist[:-1])
        call_data['extend_nav_buttons'].append([4006, "List TextBlocks", True, backref])
    else:
        call_data['extend_nav_buttons'].append(['manage_textblocks', "List TextBlocks", True, ''])

    page_data['st1:hidden_field1'] = edited_textblock
    page_data['sta1:hidden_field1'] = edited_textblock
    page_data['sb1:hidden_field1'] = edited_textblock
    page_data['sb2:hidden_field1'] = edited_textblock
    page_data['st2:hidden_field1'] = edited_textblock
    page_data[("adminhead","page_head","large_text")] = "Edit TextBlock : " + edited_textblock
    page_data['ts1:para_text'] = _list_to_string(result[edited_textblock])
    # get default language textblock_lang
    langsplit = language.split('-')
    textblock_lang_list = result[edited_textblock]
    if not textblock_lang_list:
        raise FailPage("No language has been found for the TextBlock reference")
    if editedproj.default_language in textblock_lang_list:
        textblock_lang = editedproj.default_language
    elif language in textblock_lang_list:
        textblock_lang = language
    elif langsplit[0] in textblock_lang_list:
        textblock_lang = langsplit[0]
    elif default_language in textblock_lang_list:
        textblock_lang = default_language
    elif 'en' in textblock_lang_list:
        textblock_lang = 'en'
    else:
        textblock_lang = textblock_lang_list[0]
    if not textblock_lang:
        raise FailPage("No language has been found for the TextBlock reference")
    # get submitted textblock language
    if 'language' in call_data:
        textblock_language = call_data['language'].lower()
        textblock_text = accesstextblocks.get_exact_text(edited_textblock, textblock_language)
        if textblock_text is None:
            page_data['sp1:para_text'] = "No text in this language has been found, edit and submit the text below to set this language text\n"
    else:
        textblock_language = textblock_lang
        textblock_text = accesstextblocks.get_exact_text(edited_textblock, textblock_language)
        if textblock_text is None:
            raise FailPage("Failed to find text for the TextBlock reference")

    page_data['st1:input_text'] = textblock_language
    page_data['sta1:hidden_field2'] = textblock_language
    page_data['sb1:hidden_field2'] = textblock_language
    if 'text' in call_data:
        input_text = call_data['text']
    else:
        input_text = accesstextblocks.get_text(edited_textblock, (textblock_language,default_language))
    if input_text is None:
        page_data['sta1:input_text'] = ''
    else:
        page_data['sta1:input_text'] = input_text
    # should delete language be shown
    if (len(textblock_lang_list) < 2) or (textblock_text is None):
        page_data['sb1:show'] = False
    else:
        page_data['sb1:show'] = True


def submit_new_textblock(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "A new textblock is to be created"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    if "new_textblock_ref" not in call_data:
        raise ValidateError(message='Invalid call')

    new_textblock_ref = call_data['new_textblock_ref']
    if not new_textblock_ref:
        raise FailPage(message="Invalid reference")

    if _TB.search(new_textblock_ref):
        raise FailPage(message="Invalid reference")

    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    result = accesstextblocks.get_textref_languages()
    # result is a dictionary {textref: [languages],...}
    if not new_textblock_ref in result:
        # A new TextBlock is to be created
        try:
            accesstextblocks.set_text("Insert text here", new_textblock_ref, editedproj.default_language)
        except:
            raise FailPage(message = "Failed to write to the textblocks database")
    # store the reference, as this goes to textblock edit responder which requires this data
    call_data['textblock'] = new_textblock_ref


def submit_text(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Set the text of the textblock"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    if "textblock" not in call_data:
        raise ValidateError(message='Invalid call - no textblock reference')
    if "language" not in call_data:
        raise ValidateError(message='Invalid call - no language set')
    if "text" not in call_data:
        raise ValidateError(message='Invalid call - no text set')
    # set the text and language in this textblock text
    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    accesstextblocks.set_text(call_data['text'], call_data['textblock'], call_data['language'])
    call_data['status'] = "TextBlock updated"


def submit_delete_language(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Delete a language"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    if "textblock" not in call_data:
        raise ValidateError(message='Invalid call - no textblock reference')
    if "delete_language" not in call_data:
        raise ValidateError(message='Invalid call - no language to delete set')
    # request a language deletion
    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    result = accesstextblocks.get_textref_languages()
    # result is a dictionary {textref: [languages],...}
    if call_data['textblock'] not in result:
        raise FailPage("Failed to find the TextBlock reference")
    lang_list = result[call_data['textblock']]
    if call_data['delete_language'] not in lang_list:
        raise FailPage("Failed to find the TextBlock language")
    language = call_data['delete_language'].lower()
    if len(lang_list) < 2:
        raise FailPage("Only one language set, cannot be deleted")
    # delete the block language
    accesstextblocks.del_text(call_data['textblock'], language)
    call_data['status'] = "Language deleted"


def submit_delete_textblock(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Delete a textblock"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident
    status = False

    if "delete_textblock" not in call_data:
        raise ValidateError(message='Invalid call - no textblock reference')
    textref = call_data['delete_textblock']
    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    if not accesstextblocks.textref_exists(textref):
        call_data['status'] = "TextBlock not found"
        return
    accesstextblocks.del_textblock(textref)
    call_data['status'] = "TextBlock deleted"


def submit_copy_textblock(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Copy a textblock"

    editedproj = call_data['editedproj']
    proj_ident = editedproj.proj_ident

    if "textblock" not in call_data:
        raise ValidateError(message='Invalid call - no textblock reference')
    if "copy_textblock_ref" not in call_data:
        raise ValidateError(message='Invalid call - no new textblock reference')
    if _TB.search(call_data['copy_textblock_ref']):
        raise FailPage(message="Invalid reference")
    accesstextblocks = skilift.get_accesstextblocks(proj_ident)
    accesstextblocks.copy(call_data['textblock'], call_data['copy_textblock_ref'])
    call_data['status'] = "TextBlock ref %s copied to %s" % (call_data['textblock'], call_data['copy_textblock_ref'])


def _list_to_string(lang_list):
    string_result = ""
    if not lang_list:
        return ''
    for lang in lang_list:
        string_result += lang
        string_result += ", "
    return string_result[:-2]

