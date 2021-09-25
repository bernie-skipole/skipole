
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
    let value = this.fieldarg_in_result('hidden_field', result, fieldlist);
    if (value) {
        this.widg.attr("value", value);
        }
    };


SKIPOLE.inputforms.HiddenSessionStorage = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    if ( SKIPOLE.widget_register.hasOwnProperty("inputforms.HiddenSessionStorage") ) {
        SKIPOLE.widget_register["inputforms.HiddenSessionStorage"].push(widg_id);
        }
    else {
        SKIPOLE.widget_register["inputforms.HiddenSessionStorage"] = [widg_id];
        }
    };
SKIPOLE.inputforms.HiddenSessionStorage.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.HiddenSessionStorage.prototype.constructor = SKIPOLE.inputforms.HiddenSessionStorage;
SKIPOLE.inputforms.HiddenSessionStorage.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    if (typeof(Storage) !== "undefined") {
            // get the key, and its value from storage
            let thekey = this.fieldarg_in_result('session_key', result, fieldlist);
            let keyvalue = sessionStorage.getItem(thekey);
            if (keyvalue !== "undefined") {
                this.widg.attr("value", keyvalue);
                this.fieldvalues["session_key"] = thekey
                }
        }
    };
SKIPOLE.inputforms.HiddenSessionStorage.prototype.updatefunc = function () {
    if (typeof(Storage) !== "undefined") {
        let thekey = this.fieldvalues["session_key"];
        let keyvalue = sessionStorage.getItem(thekey);
        if (keyvalue !== "undefined") {
            this.widg.attr("value", keyvalue);
            }
        }
    };


SKIPOLE.inputforms.HiddenLocalStorage = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    if ( SKIPOLE.widget_register.hasOwnProperty("inputforms.HiddenLocalStorage") ) {
        SKIPOLE.widget_register["inputforms.HiddenLocalStorage"].push(widg_id);
        }
    else {
        SKIPOLE.widget_register["inputforms.HiddenLocalStorage"] = [widg_id];
        }
    };
SKIPOLE.inputforms.HiddenLocalStorage.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.HiddenLocalStorage.prototype.constructor = SKIPOLE.inputforms.HiddenLocalStorage;
SKIPOLE.inputforms.HiddenLocalStorage.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    if (typeof(Storage) !== "undefined") {
            // get the key, and its value from storage
            let thekey = this.fieldarg_in_result('local_key', result, fieldlist);
            let keyvalue = localStorage.getItem(thekey);
            if (keyvalue !== "undefined") {
                this.widg.attr("value", keyvalue);
                this.fieldvalues["local_key"] = thekey
                }
        }
    };
SKIPOLE.inputforms.HiddenLocalStorage.prototype.updatefunc = function () {
    if (typeof(Storage) !== "undefined") {
        let thekey = this.fieldvalues["local_key"];
        let keyvalue = localStorage.getItem(thekey);
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
    let button_text = this.fieldarg_in_result('button_text', result, fieldlist);
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
    let button_text = this.fieldarg_in_result('button_text', result, fieldlist);
    if (button_text) {
        this.widg.attr("value", button_text);
        }
    };


SKIPOLE.inputforms.Form1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.inputforms.Form1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.Form1.prototype.constructor = SKIPOLE.inputforms.Form1;
SKIPOLE.inputforms.Form1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // sets hidden fields
    this.sethiddenfields(fieldlist, result);
    };
SKIPOLE.inputforms.Form1.prototype.eventfunc = function(e) {
    SKIPOLE.skiprefresh = true;
    let selected_form = $(e.target);
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
SKIPOLE.inputforms.SubmitForm1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // sets hidden fields
    this.sethiddenfields(fieldlist, result);
    };

SKIPOLE.inputforms.SubmitForm1.prototype.eventfunc = function(e) {
    SKIPOLE.skiprefresh = true;
    let selected_form = $(e.target);
    if (!SKIPOLE.form_validate(selected_form)) {
        // prevent the submission if validation failure
        e.preventDefault();
        }
    else {
        // form validated, set please wait message on button
        let btn = $("#" + this.fieldvalues["buttonident"]);
        let buttontext = btn.attr("value");
        // set button_wait_text
        let button_wait_text = this.fieldvalues["button_wait_text"]
        if (button_wait_text) {
            btn.attr("value", button_wait_text);
            }
        // if action_json url set, call a json page
        let jsonurl = this.fieldvalues["url"];
        if (jsonurl) {
            // json url set, send data with a request for json and prevent default
            let self = this
            let widgform = this.widg.find('form');
            let senddata = widgform.serializeArray();
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
                              if (btn.attr("value") == button_wait_text) {
                                   btn.attr("value", buttontext);
                                   }
                              }
                          else {
                              // If no error received, clear any previous error
                              self.clear_error();
                              SKIPOLE.setfields(result);
                              if (btn.attr("value") == button_wait_text) {
                                   btn.attr("value", buttontext);
                                   }
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
                                  if (btn.attr("value") == button_wait_text) {
                                      btn.attr("value", buttontext);
                                      }
                                  SKIPOLE.json_failed( jqXHR, textStatus, errorThrown );
                                  }
                      });
            }
        }
    };



SKIPOLE.inputforms.SubmitForm2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.inputforms.SubmitForm2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.SubmitForm2.prototype.constructor = SKIPOLE.inputforms.SubmitForm2;
SKIPOLE.inputforms.SubmitForm2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }

    // sets hidden fields
    this.sethiddenfields(fieldlist, result);

    // session_storage
    let sessionkey = this.fieldarg_in_result('session_storage', result, fieldlist);
    if (sessionkey) {
        this.fieldvalues["session_storage"] = sessionkey;
        }
    // local_storage
    let localkey = this.fieldarg_in_result('local_storage', result, fieldlist);
    if (localkey) {
        this.fieldvalues["local_storage"] = localkey;
        }
    };

SKIPOLE.inputforms.SubmitForm2.prototype.eventfunc = function(e) {
    SKIPOLE.skiprefresh = true;
    let selected_form = $(e.target);
    if (!SKIPOLE.form_validate(selected_form)) {
        // prevent the submission if validation failure
        e.preventDefault();
        return;
        }

    // form validated, set please wait message on button
    let btn = $("#" + this.fieldvalues["buttonident"]);
    let buttontext = btn.attr("value");
    // set button_wait_text
    let button_wait_text = this.fieldvalues["button_wait_text"]
    if (button_wait_text) {
        btn.attr("value", button_wait_text);
        }

    // Get the url to call
    let url = this.fieldvalues["url"];
    if (!url) {
        url = selected_form.attr('action');
        }
    if (!url) {
        e.preventDefault();
        return;
        }

    // url set, send data
    let self = this
    let senddata = new FormData(selected_form[0]);

    let sessionkey = this.fieldvalues["session_storage"];
    let localkey = this.fieldvalues["local_storage"];

    if (sessionkey || localkey) {
        // set stored data into senddata
        if (typeof(Storage) !== "undefined") {

            if (sessionkey) {
                // get the key value from storage
                let s_keyvalue = sessionStorage.getItem(sessionkey);
                if (s_keyvalue != null) {
                    senddata.append(this.formname("session_storage"), s_keyvalue);
                    }
                }
            if (localkey) {
                // get the key value from storage
                let l_keyvalue = localStorage.getItem(localkey);
                if (l_keyvalue != null) {
                    senddata.append(this.formname("local_storage"), l_keyvalue);
                    }
                }

            }
        }


    e.preventDefault();
    // respond to json or html
    $.ajax({
          url: url,
          data: senddata,
          processData: false,
          contentType: false,
          type: 'POST',
              })
          .done(function(result, textStatus, jqXHR) {
             if (jqXHR.responseJSON) {
                  // JSON response
                  if (self.get_error(result)) {
                      // if error, set any results received from the json call
                      SKIPOLE.setfields(result);
                      if (btn.attr("value") == button_wait_text) {
                           btn.attr("value", buttontext);
                           }
                      }
                  else {
                      // If no error received, clear any previous error
                      self.clear_error();
                      SKIPOLE.setfields(result);
                      if (btn.attr("value") == button_wait_text) {
                           btn.attr("value", buttontext);
                           }
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
                          if (btn.attr("value") == button_wait_text) {
                              btn.attr("value", buttontext);
                              }
                          SKIPOLE.json_failed( jqXHR, textStatus, errorThrown );
                          }
              });
    };


SKIPOLE.inputforms.SubmitFromScript = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputforms.SubmitFromScript.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputforms.SubmitFromScript.prototype.constructor = SKIPOLE.inputforms.SubmitFromScript;
SKIPOLE.inputforms.SubmitFromScript.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // hide
    let set_hide = this.fieldarg_in_result('hide', result, fieldlist);
    if (set_hide !== undefined) {
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
SKIPOLE.inputforms.SubmitFromScript.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    if (e.type == 'submit') {

        // hidden_field1
        let hf1 = this.fieldvalues["hidden_field1"];
        if (hf1 !== undefined) {
            hf1val = new Function(hf1);
            let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field1') + "\"]";
            let isfield = this.widg.find(find_field_name);
            if (isfield.length){
                isfield.first().val(hf1val());
                }
            }

        // hidden_field2
        let hf2 = this.fieldvalues["hidden_field2"];
        if (hf2 !== undefined) {
            hf2val = new Function(hf2);
            let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field2') + "\"]";
            let isfield = this.widg.find(find_field_name);
            if (isfield.length){
                isfield.first().val(hf2val());
                }
            }

        // hidden_field3
        let hf3 = this.fieldvalues["hidden_field3"];
        if (hf3 !== undefined) {
            hf3val = new Function(hf3);
            let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field3') + "\"]";
            let isfield = this.widg.find(find_field_name);
            if (isfield.length){
                isfield.first().val(hf3val());
                }
            }

        // hidden_field4
        let hf4 = this.fieldvalues["hidden_field4"];
        if (hf4 !== undefined) {
            hf4val = new Function(hf4);
            let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field4') + "\"]";
            let isfield = this.widg.find(find_field_name);
            if (isfield.length){
                isfield.first().val(hf4val());
                }
            }

        // form submitted, so if json url set, call a json page
        let jsonurl = this.fieldvalues["url"];
        if (jsonurl) {
            let self = this;
            let widgform = $(e.target);
            let senddata = widgform.serializeArray();
            e.preventDefault();
            // respond to json or html
            $.ajax({
                  url: jsonurl,
                  data: senddata
                      })
                  .done(function(result, textStatus, jqXHR) {
                     if (jqXHR.responseJSON) {
                          // JSON response
                          SKIPOLE.setfields(result);
                          }
                     else {
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
                                  SKIPOLE.json_failed( jqXHR, textStatus, errorThrown );
                                  }
                      });
            }
        }
    };


