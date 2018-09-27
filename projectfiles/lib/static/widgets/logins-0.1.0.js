/*
####### SKIPOLE WEB FRAMEWORK #######

logins-0.1.0.js  - javascript widgets

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


SKIPOLE.logins = {};


SKIPOLE.logins.NamePasswd1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.logins.NamePasswd1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.logins.NamePasswd1.prototype.constructor = SKIPOLE.logins.NamePasswd1;
SKIPOLE.logins.NamePasswd1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var text1 = this.widg.find('input:first');
    // Check for set_input_accepted1 or set_input_errored1
    var input_accepted1 = this.fieldarg_in_result('set_input_accepted1', result, fieldlist);
    this.set_accepted(text1, input_accepted1);
    var input_errored1 = this.fieldarg_in_result('set_input_errored1', result, fieldlist);
    this.set_errored(text1, input_errored1);
    // input_text1
    var input_text1 = this.fieldarg_in_result('input_text1', result, fieldlist);
    if (input_text1) {
        text1.val(input_text1);
        }
    var text2 = this.widg.find('input:eq(1)');
    // Check for set_input_accepted2 or set_input_errored2
    var input_accepted2 = this.fieldarg_in_result('set_input_accepted2', result, fieldlist);
    this.set_accepted(text2, input_accepted2);
    var input_errored2 = this.fieldarg_in_result('set_input_errored2', result, fieldlist);
    this.set_errored(text2, input_errored2);
    // input_text2
    var input_text2 = this.fieldarg_in_result('input_text2', result, fieldlist);
    if (input_text2) {
        text2.val(input_text2);
        }
    };
SKIPOLE.logins.NamePasswd1.prototype.eventfunc = function (e) {
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
                var self = this
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
                                  // enable input event, which is used to clear set_accepted class on input
                                  self.widg.on('input', function(e) {self.eventfunc(e)});
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
    else if (e.type == 'input'){
        // text changed in input field
        this.widg.off(e);
        this.set_accepted($(e.target),false);
        }
    };
SKIPOLE.logins.NamePasswd1.prototype.clear_error = function() {
    if (!this.display_errors) {
        return;
        }
    SKIPOLE.BaseWidget.prototype.clear_error.call(this);
    var text1 = this.widg.find('input:first');
    this.set_errored(text1, false);
    var text2 = this.widg.find('input:eq(1)');
    this.set_errored(text2, false);
    };



SKIPOLE.logins.Pin4 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.logins.Pin4.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.logins.Pin4.prototype.constructor = SKIPOLE.logins.Pin4;
SKIPOLE.logins.Pin4.prototype.setvalues = function (fieldlist, result) {
    /* This widget accepts fields - hide */
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    if (this.check_error(fieldlist, result)) {
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
SKIPOLE.logins.Pin4.prototype.show_error = function (error_message) {
    if (!this.widg_id) {
        return;
        }
    if (!error_message) {
        error_message = this.error_message;
        }
    if (!error_message) {
        error_message = "Unknown Error";
        }
    var the_widg = this.widg;
    the_widg.attr("data-status", "error");
    // get error para to insert error message
    var inner_div = the_widg.find(':first');
    var error_div = inner_div.find(':first');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.logins.Pin4.prototype.clear_error = function() {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" );
        }
    var inner_div = the_widg.find(':first');
    var error_div = inner_div.find(':first');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };
