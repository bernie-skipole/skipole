####### SKIPOLE WEB FRAMEWORK #######
#
# info_tuple.py  - named tuples used by other modules
#
# This file is part of the Skipole web framework
#
# Date : 20180612
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

"""
named tuples used by other modules
"""

from collections import namedtuple


ProjectInfo = namedtuple('ProjectInfo', ['project', 'version', 'brief', 'path', 'default_language', 'subprojects', 'json_file', 'tar_path'])

ItemInfo = namedtuple('ItemInfo', ['project', 'project_version', 'itemnumber', 'item_type', 'name', 'brief', 'path', 'label_list', 'change', 'parentfolder_number', 'restricted'])

PartInfo = namedtuple('PartInfo', ['project', 'pagenumber', 'page_part', 'section_name', 'name', 'location', 'part_type', 'brief'])

PageInfo = namedtuple('PageInfo', ['name', 'number', 'restricted', 'brief', 'item_type', 'responder', 'enable_cache', 'change', 'parentfolder_number'])

FolderInfo = namedtuple('FolderInfo', ['name', 'number', 'restricted', 'brief', 'contains_pages', 'contains_folders', 'change'])

WidgetInfo = namedtuple('WidgetInfo', ['project', 'pagenumber', 'section_name', 'name', 'location', 'containers', 'display_errors', 'brief'])

PageElement = namedtuple('PageElement', ['project', 'pagenumber', 'pchange', 'location', 'page_part', 'part_type', 'tag_name', 'brief', 'hide_if_empty', 'attribs'])

PageTextBlock = namedtuple('PageTextBlock', ['project', 'pagenumber', 'pchange', 'location', 'textref', 'failmessage', 'escape', 'linebreaks', 'decode'])

WidgFieldInfo = namedtuple('WidgFieldInfo', ['tuple_widgfield', 'str_widgfield', 'str_comma_widgfield'])

PlaceHolderInfo = namedtuple('PlaceHolderInfo', ['project', 'pagenumber', 'section_name', 'alias', 'brief', 'multiplier', 'mtag'])

SectionElement = namedtuple('SectionElement', ['project', 'section_name', 'schange', 'location', 'part_type', 'tag_name', 'brief', 'show', 'hide_if_empty', 'attribs'])

SectionTextBlock = namedtuple('SectionTextBlock', ['project', 'section_name', 'schange', 'location', 'textref', 'failmessage', 'escape', 'linebreaks', 'decode'])


WidgetDescription = namedtuple('WidgetDescription', ['modulename', 'classname', 'brief', 'fields', 'containers', 'illustration',
                                                     'fields_single', 'fields_list', 'fields_table', 'fields_dictionary', 'parent_widget', 'parent_container'])
# 'fields' is a list of lists: [ field arg, field ref]
# 'containers' is the number of containers in the widget, 0 for none


FieldDescription = namedtuple('FieldDescription', ['field_arg', 'field_ref', 'field_type', 'valdt', 'jsonset', 'cssclass', 'cssstyle'])

ContainerInfo = namedtuple('ContainerInfo', ['container', 'container_ref', 'empty'])


ResponderInfo = namedtuple('ResponderInfo', ['responder',
                                             'module_name',
                                             'widgfield_required',
                                             'widgfield',
                                             'alternate_ident_required',
                                             'alternate_ident',
                                             'target_ident_required',
                                             'target_ident',
                                             'allowed_callers_required',
                                             'allowed_callers',
                                             'validate_option_available',
                                             'validate_option',
                                             'validate_fail_ident',
                                             'submit_option_available',
                                             'submit_option',
                                             'submit_required',
                                             'submit_list',
                                             'fail_ident',
                                             'field_options',
                                             'field_values_list',
                                             'field_list',
                                             'single_field_value',
                                             'single_field'
                                            ])


ValidatorInfo = namedtuple('ValidatorInfo', ['validator',
                                             'module_name',
                                             'message',
                                             'message_ref',
                                             'displaywidget',
                                             'allowed_values',
                                             'val_args'
                                            ])




