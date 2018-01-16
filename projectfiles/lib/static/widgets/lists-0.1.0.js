/*
####### SKIPOLE WEB FRAMEWORK #######

 lists-0.1.0.js  - javascript widgets

 This file is part of the Skipole web framework

 Date : 20180116

 Author : Bernard Czenkusz
 Email  : bernie@skipole.co.uk


   Copyright 2018 Bernard Czenkusz

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


SKIPOLE.lists = {};

SKIPOLE.lists.UList1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.lists.UList1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.lists.UList1.prototype.constructor = SKIPOLE.lists.UList1;
SKIPOLE.lists.UList1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    var fieldvalues = this.fieldvalues;
    // contents
    var contents = this.fieldarg_in_result('contents', result, fieldlist);
    // the class of the elements
    var even_class = fieldvalues["even_class"];
    var odd_class = fieldvalues["odd_class"];

    if (contents) {
        // If a request to renew the list is recieved, this block
        // empties the existing list, and re-draws it
        var rows = contents.length;
        // empty the list
        the_widg.empty();
        // and now start filling it again
        var htmlcontent = "";
        for (row = 0; row < rows; row++) {
            // for each row
            if (even_class && (row % 2)) {
                htmlcontent += "<li class = \"" + even_class + "\">";
                }
            else if (odd_class && (!(row % 2))) {
                htmlcontent += "<li class = \"" + odd_class + "\">";
                }
            else {
                htmlcontent += "<li>";
                }
            htmlcontent += SKIPOLE.textbr(contents[row]);
            // close the cell
            htmlcontent += "</li>";
            }
        the_widg.html(htmlcontent);
        }
    };


