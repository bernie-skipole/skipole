/*
####### SKIPOLE WEB FRAMEWORK #######

 inputforms-0.1.0.js  - javascript widgets

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


SKIPOLE.inputforms = {};

SKIPOLE.inputforms.HiddenField = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputforms.HiddenField.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.HiddenField.prototype.constructor = SKIPOLE.inputforms.HiddenField;
SKIPOLE.inputforms.HiddenField.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // value
    var value = this.fieldarg_in_result('hidden_field', result, fieldlist);
    if (value) {
        this.widg.attr("value", value);
        }
    };


SKIPOLE.inputforms.HiddenSessionStorage = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputforms.HiddenSessionStorage.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.HiddenSessionStorage.prototype.constructor = SKIPOLE.inputforms.HiddenSessionStorage;
SKIPOLE.inputforms.HiddenSessionStorage.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    if (typeof(Storage) !== "undefined") {
            // get the key, and its value from storage
            var thekey = this.fieldarg_in_result('session_key', result, fieldlist);
            var keyvalue = sessionStorage.getItem(thekey);
            if (keyvalue !== "undefined") {
                this.widg.attr("value", keyvalue);
                }
        }
    };
SKIPOLE.inputforms.HiddenSessionStorage.prototype.updatefunc = function (arg) {
    if (typeof(Storage) !== "undefined") {
        var keyvalue = sessionStorage.getItem(arg);
        if (keyvalue !== "undefined") {
            this.widg.attr("value", keyvalue);
            }
        }
    };


SKIPOLE.inputforms.HiddenLocalStorage = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputforms.HiddenLocalStorage.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.HiddenLocalStorage.prototype.constructor = SKIPOLE.inputforms.HiddenLocalStorage;
SKIPOLE.inputforms.HiddenLocalStorage.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    if (typeof(Storage) !== "undefined") {
            // get the key, and its value from storage
            var thekey = this.fieldarg_in_result('local_key', result, fieldlist);
            var keyvalue = localStorage.getItem(thekey);
            if (keyvalue !== "undefined") {
                this.widg.attr("value", keyvalue);
                }
        }
    };
SKIPOLE.inputforms.HiddenLocalStorage.prototype.updatefunc = function (arg) {
    if (typeof(Storage) !== "undefined") {
        var keyvalue = localStorage.getItem(arg);
        if (keyvalue !== "undefined") {
            this.widg.attr("value", keyvalue);
            }
        }
    };


SKIPOLE.inputforms.SubmitButton1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputforms.SubmitButton1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.SubmitButton1.prototype.constructor = SKIPOLE.inputforms.SubmitButton1;
SKIPOLE.inputforms.SubmitButton1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // button_text
    var button_text = this.fieldarg_in_result('button_text', result, fieldlist);
    if (button_text) {
        this.widg.attr("value", button_text);
        }
    };


SKIPOLE.inputforms.SubmitButton2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputforms.SubmitButton2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.SubmitButton2.prototype.constructor = SKIPOLE.inputforms.SubmitButton2;
SKIPOLE.inputforms.SubmitButton2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // button_text
    var button_text = this.fieldarg_in_result('button_text', result, fieldlist);
    if (button_text) {
        this.widg.attr("value", button_text);
        }
    };


SKIPOLE.inputforms.Form1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.inputforms.Form1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.Form1.prototype.constructor = SKIPOLE.inputforms.Form1;
SKIPOLE.inputforms.Form1.prototype.eventfunc = function(e) {
    var selected_form = $(e.target);
    if (!SKIPOLE.form_validate(selected_form)) {
        // prevent the submission if validation failure
        e.preventDefault();
        }
    };


SKIPOLE.inputforms.SubmitForm1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.inputforms.SubmitForm1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.SubmitForm1.prototype.constructor = SKIPOLE.inputforms.SubmitForm1;
SKIPOLE.inputforms.SubmitForm1.prototype.eventfunc = function(e) {
    var selected_form = $(e.target);
    if (!SKIPOLE.form_validate(selected_form)) {
        // prevent the submission if validation failure
        e.preventDefault();
        }
    else {
        // form validated, so if action_json url set, call a json page
        var jsonurl = this.fieldvalues["url"];
        if (jsonurl) {
            // json url set, send data with a request for json and prevent default
            var self = this
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
        }
    };


