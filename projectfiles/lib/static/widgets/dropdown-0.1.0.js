/*
####### SKIPOLE WEB FRAMEWORK #######

 dropdown-0.1.0.js  - javascript widgets

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



SKIPOLE.dropdown = {};


SKIPOLE.dropdown.DropDown1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.dropdown.DropDown1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.dropdown.DropDown1.prototype.constructor = SKIPOLE.dropdown.DropDown1;


SKIPOLE.dropdown.SubmitDropDown1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.dropdown.SubmitDropDown1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.dropdown.SubmitDropDown1.prototype.constructor = SKIPOLE.dropdown.SubmitDropDown1;
SKIPOLE.dropdown.SubmitDropDown1.prototype.eventfunc = function(e) {
    // if action_json url set, call a json page
    var jsonurl = this.fieldvalues["url"];
    if (jsonurl) {
        // json url set, send data with a request for json and prevent default
        var self = this;
        var widgform = this.widg.find('form');
        var senddata = widgform.serializeArray();
        $.getJSON(jsonurl, senddata).done(function(result){
            if (!self.get_error(result)) {
                // If no error received, clear any previous error
                self.clear_error();
                }
            SKIPOLE.setfields(result);
            });
        e.preventDefault();
        }
    };
SKIPOLE.dropdown.SubmitDropDown1.prototype.setvalues = function (fieldlist, result) {
    /* This widget accepts fields - hide */
   if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    var set_hide = this.fieldarg_in_result('hide', result, fieldlist);
    if (set_hide != undefined) {
        if (set_hide) {
            if (the_widg.is(":visible")) {
                the_widg.fadeOut('slow');
                }
            }
        else {
            if (!(the_widg.is(":visible"))) {
                the_widg.fadeIn('slow');
                 }
            }
        }
    };

