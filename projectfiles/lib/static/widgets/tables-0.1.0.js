/*
####### SKIPOLE WEB FRAMEWORK #######

 tables-0.1.0.js  - javascript widgets

 This file is part of the Skipole web framework

 Date : 20150501

 Author : Bernard Czenkusz
 Email  : bernie@skipole.co.uk


   Copyright 2015 Bernard Czenkusz

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/


SKIPOLE.tables = {};

SKIPOLE.tables.ColorTable1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.tables.ColorTable1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.tables.ColorTable1.prototype.constructor = SKIPOLE.tables.ColorTable1;


SKIPOLE.tables.TwoColTable1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.tables.TwoColTable1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.tables.TwoColTable1.prototype.constructor = SKIPOLE.tables.TwoColTable1;
SKIPOLE.tables.TwoColTable1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    // col1 and col2
    var col1 = this.fieldarg_in_result('col1', result, fieldlist);
    var col2 = this.fieldarg_in_result('col2', result, fieldlist);
    var self = this;
    var index = 0;
    var header = false;
    if (the_widg.find('th')) {
        header = true;
        }
    the_widg.find('tr').each(function() {
        if (header) {
            header = false;
            }
        else {
            // for each row
            var cells = $(this).children();
            if (col1) {
                $(cells[0]).text(col1[index]);
                 }
            if (col2) {
               $(cells[1]).text(col2[index])
                }
             index=index+1;
            }
        })
    };


SKIPOLE.tables.TextBlockTable2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.tables.TextBlockTable2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.tables.TextBlockTable2.prototype.constructor = SKIPOLE.tables.TextBlockTable2;


SKIPOLE.tables.ButtonTextBlockTable1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.tables.ButtonTextBlockTable1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.tables.ButtonTextBlockTable1.prototype.constructor = SKIPOLE.tables.ButtonTextBlockTable1;




