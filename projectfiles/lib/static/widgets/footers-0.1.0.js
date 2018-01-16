/*
####### SKIPOLE WEB FRAMEWORK #######

 footers-0.1.0.js  - javascript widgets

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


SKIPOLE.footers = {};

SKIPOLE.footers.SimpleFooter = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.footers.SimpleFooter.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.footers.SimpleFooter.prototype.constructor = SKIPOLE.footers.SimpleFooter;
SKIPOLE.footers.SimpleFooter.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // footer_text
    var footer_text = this.fieldarg_in_result('footer_text', result, fieldlist);
    if (footer_text) {
	    var textident = this.fieldvalues["textident"];
	    if (!textident) {
	        return;
            }
	    $('#'+textident).text(footer_text);
        }
    };




