/*
####### SKIPOLE WEB FRAMEWORK #######

 textarea-0.1.0.js  - javascript widgets

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



SKIPOLE.textarea = {};


SKIPOLE.textarea.SubmitTextArea = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.textarea.SubmitTextArea.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.textarea.SubmitTextArea.prototype.constructor = SKIPOLE.textarea.SubmitTextArea;
SKIPOLE.textarea.SubmitTextArea.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
     /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // input_text
    var input_text = this.fieldarg_in_result('input_text', result, fieldlist);
    textarea = this.widg.find('textarea').filter(":first")
    textarea.text(input_text);
    };


SKIPOLE.textarea.TextArea1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.textarea.TextArea1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.textarea.TextArea1.prototype.constructor = SKIPOLE.textarea.TextArea1;
SKIPOLE.textarea.TextArea1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
     // input_text
    var input_text = this.fieldarg_in_result('input_text', result, fieldlist);
    if (input_text) {
        this.widg.text(input_text);
        }
    };


SKIPOLE.textarea.TextArea2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.textarea.TextArea2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.textarea.TextArea2.prototype.constructor = SKIPOLE.textarea.TextArea2;
SKIPOLE.textarea.TextArea2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // input_text
    var text_input = this.widg.find('textarea');
    var input_text = this.fieldarg_in_result('input_text', result, fieldlist);
    if (input_text) {
        text_input.text(input_text);
        }
    };

