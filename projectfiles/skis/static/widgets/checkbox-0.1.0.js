/*
####### SKIPOLE WEB FRAMEWORK #######

 checkbox-0.1.0.js  - javascript widgets

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


SKIPOLE.checkbox = {};


SKIPOLE.checkbox.CheckBox1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.checkbox.CheckBox1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.checkbox.CheckBox1.prototype.constructor = SKIPOLE.checkbox.CheckBox1;
SKIPOLE.checkbox.CheckBox1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // checked
    var checked_value = this.fieldarg_in_result('checked', result, fieldlist);
    if (checked_value === true) {
        this.widg.find('input').prop('checked', true);
        }
    if (checked_value === false) {
        this.widg.find('input').prop('checked', false);
        }
    };


SKIPOLE.checkbox.CheckBox2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.checkbox.CheckBox2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.checkbox.CheckBox2.prototype.constructor = SKIPOLE.checkbox.CheckBox2;
SKIPOLE.checkbox.CheckBox2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // checked
    var checked_value = this.fieldarg_in_result('checked', result, fieldlist);
    if (checked_value === true) {
        this.widg.find('input').prop('checked', true);
        }
    if (checked_value === false) {
        this.widg.find('input').prop('checked', false);
        }
    };


SKIPOLE.checkbox.CheckedText = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.checkbox.CheckedText.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.checkbox.CheckedText.prototype.constructor = SKIPOLE.checkbox.CheckedText;
SKIPOLE.checkbox.CheckedText.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // checked
    var checked_value = this.fieldarg_in_result('checked', result, fieldlist);
    if (checked_value === true) {
        this.widg.find('input[type="checkbox"]').prop('checked', true);
        this.widg.find('input[type="text"]').prop('disabled',false);
        }
    if (checked_value === false) {
        this.widg.find('input[type="checkbox"]').prop('checked', false);
        this.widg.find('input[type="text"]').prop('disabled',true);
        }
    };


SKIPOLE.checkbox.CheckInputs = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.checkbox.CheckInputs.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.checkbox.CheckInputs.prototype.constructor = SKIPOLE.checkbox.CheckInputs;
SKIPOLE.checkbox.CheckInputs.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // checked
    var checked_value = this.fieldarg_in_result('checked', result, fieldlist);
    if (checked_value === true) {
        this.widg.find('input[type="checkbox"]').first().prop('checked', true);
        this.widg.find('input[type="text"]').prop('disabled',false);
        }
    if (checked_value === false) {
        this.widg.find('input[type="checkbox"]').first().prop('checked', false);
        this.widg.find('input[type="text"]').prop('disabled',true);
        }
    };


SKIPOLE.checkbox.SubmitCheckBox1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.checkbox.SubmitCheckBox1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.checkbox.SubmitCheckBox1.prototype.constructor = SKIPOLE.checkbox.SubmitCheckBox1;
SKIPOLE.checkbox.SubmitCheckBox1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // checked
    var checked_value = this.fieldarg_in_result('checked', result, fieldlist);
    if (checked_value === true) {
        this.widg.find('input[type="checkbox"]').prop('checked', true);
        }
    if (checked_value === false) {
        this.widg.find('input[type="checkbox"]').prop('checked', false);
        }
    // hide
    var set_hide = this.fieldarg_in_result('hide', result, fieldlist);
    if (set_hide != undefined) {
        if (set_hide) {
            if (this.widg.is(":visible")) {
                this.widg.fadeOut('slow');
                }
            }
        else {
            if (!(this.widg.is(":visible"))) {
                this.widg.fadeIn('slow');
                 }
            }
        }
    };
SKIPOLE.checkbox.SubmitCheckBox1.prototype.eventfunc = function (e) {
    if (e.type == 'submit') {
        // form submitted
        if (!SKIPOLE.form_validate(this.widg)) {
            // prevent the submission if validation failure
            e.preventDefault();
            }
        else {
            // form validated, so if json url set, call a json page
            var jsonurl = this.fieldvalues["url"];
            if (jsonurl) {
                var self = this;
                var widgform = this.widg.find('form');
                var senddata = widgform.serializeArray();
                e.preventDefault();
                // respond to json or html
                $.ajax({
                      url: jsonurl,
                      data: senddata
                          })
                      .done(function(result, textStatus, jqXHR) {
                         if (jqXHR.responseJSON) {
                              // JSON response
                              if (self.get_error(result)) {
                                  // if error, set any results received from the json call
                                  SKIPOLE.setfields(result);
                                  }
                              else {
                                  // If no error received, clear any previous error
                                  self.clear_error();
                                  SKIPOLE.setfields(result);
                                  }
                               } else {
                                  // html response
                                  document.open();
                                  document.write(result);
                                  document.close();
                                  }
                          })
                      .fail(function( jqXHR, textStatus, errorThrown ) {
                                  if (jqXHR.status == 400 || jqXHR.status == 404 || jqXHR.status == 500)  {
                                      document.open();
                                      document.write(jqXHR.responseText);
                                      document.close();
                                      }
                                  else {
                                      alert(errorThrown);
                                      }
                          });
                }
            }
        }
    };


