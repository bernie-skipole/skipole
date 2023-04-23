
var SKIPOLE = {};

SKIPOLE.widgets = {};
SKIPOLE.validators = {};
SKIPOLE.sections = [];
SKIPOLE.skiprefresh = false;


SKIPOLE.restorepagepos = function() {
    // restore window position from last position stored
    if(typeof(Storage) !== "undefined") {
        let pageidentarray = SKIPOLE.identdata.split('_');
        let x_pos = pageidentarray[0] + '_' + pageidentarray[1] + '_x';
        let y_pos = pageidentarray[0] + '_' + pageidentarray[1] + '_y';
        if (sessionStorage.getItem(y_pos)) {
            // Restore the y position of the window
            $(window).scrollTop(parseInt(sessionStorage.getItem(y_pos)));
            }
        if (sessionStorage.getItem(x_pos)) {
            // Restore the x position of the window
            $(window).scrollLeft(parseInt(sessionStorage.getItem(x_pos)));
            }
        }
    };


SKIPOLE.refreshjson = function( target ) {
     /* called by setInterval when a page needs regular updating */
     if (SKIPOLE.skiprefresh) {
         SKIPOLE.skiprefresh = false;
         return;
         }
     $.getJSON(target, "ident=" + SKIPOLE.identdata)
         .done(function(result){
                SKIPOLE.setfields(result);
               })
         .fail(function(){
                 if (SKIPOLE.CatchToHTML) {
                     // Calls the URL given by "CatchToHTML"
                     window.location.href = SKIPOLE.CatchToHTML + "?ident=" + SKIPOLE.identdata;
                     }
                 else {
                     alert(err.message);
                     }
               })
    };


SKIPOLE.inallowedlist =  function (item, allowed_values) {
    /* Fail if no allowed values given, otherwise item must be in allowed values */
    if (allowed_values.length === 0) {
        return false;
        }
    let regstring = '';
    for (let i = 0; i < allowed_values.length; i++) {
        if (i < allowed_values.length -1) {
            regstring += '^' + allowed_values[i] + "$|";
            }
        else {
            regstring += '^' + allowed_values[i] + "$";
            }
        }
    let reg = new RegExp(regstring);
    return reg.test(item);
    }



SKIPOLE.setfields = function(result) {
    try {
       // result is the contents of a json page listing widgfields and values
       if ("ident_data" in result) {
           // set the value of SKIPOLE.identdata
           let oldidentdata = SKIPOLE.identdata;
           let pageidentarray = SKIPOLE.identdata.split('_');
           // set identdata to projectname_pagenumber_ident_data
           SKIPOLE.identdata = pageidentarray[0] + '_' + pageidentarray[1] + '_' + result["ident_data"];
           // set this in all hidden input 'ident' fields
           $("input[name='ident']:hidden").attr("value", SKIPOLE.identdata);
           // and in all url get 'ident' fields
           let old_string = "?ident=" + oldidentdata
           let new_string = "?ident=" + SKIPOLE.identdata
           $("a[href*='?ident=']").each(function(){
               // Update the ?ident= part of the url to the new ident_data string
               $(this).attr('href',$(this).attr('href').replace(old_string,new_string));
               });
           }
       if ("ClearAllErrors" in result) {
           // Clear errors in the page
           SKIPOLE.clear_all_errors();
           }
       if ("CatchToHTML" in result) {
           // Set the SKIPOLE.CatchToHTML variable to the given URL
           SKIPOLE.CatchToHTML = result["CatchToHTML"];
           }
       if ("throw" in result) {
           // create a throw with the given message
           throw new Error(result["throw"]);
           }
       if ("JSONtoHTML" in result) {
           // Calls the URL given by "JSONtoHTML"
           window.location.href = result["JSONtoHTML"] + "?ident=" + SKIPOLE.identdata;
           return;
           }
       if ("IntervalTarget" in result) {
           // Set the SKIPOLE.IntervalTarget variable to the given URL
           if (SKIPOLE.interval_id) {
               clearInterval(SKIPOLE.interval_id);
               SKIPOLE.interval_id=null;
               }
           SKIPOLE.IntervalTarget = result["IntervalTarget"];
           if(SKIPOLE.interval && SKIPOLE.IntervalTarget) {
              SKIPOLE.interval_id = setInterval(SKIPOLE.refreshjson, SKIPOLE.interval*1000, SKIPOLE.IntervalTarget);
              }
           }
       if ("interval" in result) {
           // Set the SKIPOLE.interval variable
           if (SKIPOLE.interval_id) {
               clearInterval(SKIPOLE.interval_id);
               SKIPOLE.interval_id=null;
               }
           SKIPOLE.interval = result["interval"];
           if(SKIPOLE.interval && SKIPOLE.IntervalTarget) {
              SKIPOLE.interval_id = setInterval(SKIPOLE.refreshjson, SKIPOLE.interval*1000, SKIPOLE.IntervalTarget);
              }
           }
       if ("sessionStorage" in result) {
           // set the session storage data
            if (typeof(Storage) !== "undefined") {
                for (const key in result["sessionStorage"]) {
                   sessionStorage.setItem(key, result["sessionStorage"][key]);
                   }
               // updates the value in any inputforms.HiddenSessionStorage widget
               if ( SKIPOLE.widget_register.hasOwnProperty("inputforms.HiddenSessionStorage") ) {
                    let hsswidgets = SKIPOLE.widget_register["inputforms.HiddenSessionStorage"].length;
                    // for each HiddenSessionStorage registered, call its updatefunc method
                    for (let hsswidget = 0; hsswidget < hsswidgets; hsswidget++) {
                        // for each hsswidget in the register
                        SKIPOLE.widgets[SKIPOLE.widget_register["inputforms.HiddenSessionStorage"][hsswidget]].updatefunc();
                        }
                    }
                }
           }
       if ("localStorage" in result) {
           // set the local storage data
            if (typeof(Storage) !== "undefined") {
                for (const key in result["localStorage"]) {
                   localStorage.setItem(key, result["localStorage"][key]);
                   }
               // updates the value in any inputforms.HiddenLocalStorage widget
               if ( SKIPOLE.widget_register.hasOwnProperty("inputforms.HiddenLocalStorage") ) {
                    let hlswidgets = SKIPOLE.widget_register["inputforms.HiddenLocalStorage"].length;
                    // for each HiddenLocalStorage registered, call its updatefunc method
                    for (let hlswidget = 0; hlswidget < hlswidgets; hlswidget++) {
                        // for each hlswidget in the register
                        SKIPOLE.widgets[SKIPOLE.widget_register["inputforms.HiddenLocalStorage"][hlswidget]].updatefunc();
                        }
                    }
                }
           }
       if ("environ" in result) {
           // displays the environ in any debug_tools.ShowEnviron widget
           if ( SKIPOLE.widget_register.hasOwnProperty("debug_tools.ShowEnviron") ) {
                let showenvirons = SKIPOLE.widget_register["debug_tools.ShowEnviron"].length;
                // for each ShowEnviron registered, call its updatefunc method
                for (let showenviron = 0; showenviron < showenvirons; showenviron++) {
                    // for each showenviron in the register
                    SKIPOLE.widgets[SKIPOLE.widget_register["debug_tools.ShowEnviron"][showenviron]].updatefunc(result["environ"]);
                    }
                }
           }
       if ("call_data" in result) {
           // displays the call_data dictionary in any debug_tools.ShowCallData widget
           if ( SKIPOLE.widget_register.hasOwnProperty("debug_tools.ShowCallData") ) {
                let showthem = SKIPOLE.widget_register["debug_tools.ShowCallData"].length;
                // for each ShowCallData registered, call its updatefunc method
                for (let showit = 0; showit < showthem; showit++) {
                    // for each showenviron in the register
                    SKIPOLE.widgets[SKIPOLE.widget_register["debug_tools.ShowCallData"][showit]].updatefunc(result["call_data"]);
                    }
                }
           }
       if ("ident_list" in result) {
           // displays the identlist in any debug_tools.ShowResponders widget
           if ( SKIPOLE.widget_register.hasOwnProperty("debug_tools.ShowResponders") ) {
                let showresponders = SKIPOLE.widget_register["debug_tools.ShowResponders"].length;
                // for each ShowResponders registered, call its updatefunc method
                for (let showresponder = 0; showresponder < showresponders; showresponder++) {
                    // for each showresponder in the register
                    SKIPOLE.widgets[SKIPOLE.widget_register["debug_tools.ShowResponders"][showresponder]].updatefunc(result["ident_list"]);
                    }
                }
           }
       if ("show_error" in result) {
           if (SKIPOLE.default_error_widget) {
               result[SKIPOLE.default_error_widget + ":show_error"] = result["show_error"];
               }
           }
       if ("backcol" in result) {
         if (result["backcol"]) {
             $("html").attr("style", "background-color: "+result["backcol"]);
             }
         else {
             $("html").removeAttr("style");
             }
         }
       if ("lang" in result) {
         if (result["lang"]) {
             $("html").attr("lang", result["lang"]);
             }
         else {
             $("html").removeAttr("lang");
             }
         }
       if ("body_class" in result) {
         if (result["body_class"]) {
             $("body").attr("class", result["body_class"]);
             }
         else {
             $("body").removeAttr("class");
             }
         }
       let widg_fields = {};
       // widg_fields will be a dictionary of widget id: list of json set fields
       for (const widgfield in result) {
           // widgfield parameters
           if (!widgfield.includes(":")) {
               continue;
               }
           let splitwidgfield = widgfield.split(":");
           let widg_id = splitwidgfield[0];

           if (widg_id in SKIPOLE.widgets) {
               if (!(widg_id in widg_fields)) {
                   widg_fields[widg_id] = [];
                   }
               widg_fields[widg_id].push(splitwidgfield[1]);
               continue;
               }
           // section parameters
           if (SKIPOLE.sections.indexOf(widg_id) > -1) {
               if (splitwidgfield[1] == "section_class") {
                   if (result[widgfield]) {
                       $("#"+widg_id).attr("class", result[widgfield]);
                       }
                   else {
                       $("#"+widg_id).removeAttr("class");
                       }
                   }
               if (splitwidgfield[1] == "hide") {
                   let sectionpart = $("#"+widg_id);
                   if (result[widgfield]) {
                       if (sectionpart.is(":visible")) {
                           sectionpart.fadeOut('slow');
                           }
                       }
                   else {
                       if (!(sectionpart.is(":visible"))) {
                           sectionpart.fadeIn('slow');
                           }
                       }
                   }


               }
            }

        // Now set the widget values, after first setting widget_class and widget_style - which all widgets have
        for (const widg_ident in widg_fields) {
            let fieldlist = widg_fields[widg_ident];
            let thiswidget = SKIPOLE.widgets[widg_ident]
            // If given, update the widget_class and widget_style in fieldvalues, so they are available
            // to thiswidget.setvalues even if they have been changed by JSON call
            let widget_class = thiswidget.fieldarg_in_result('widget_class', result, fieldlist);
            if (widget_class != undefined) {
                if (widget_class) {
                    $("#"+widg_ident).attr("class", widget_class);
                    thiswidget.fieldvalues["widget_class"] = widget_class;
                    }
                else {
                    $("#"+widg_ident).removeAttr("class");
                    thiswidget.fieldvalues["widget_class"] = '';
                    }
                }
            let widget_style = thiswidget.fieldarg_in_result('widget_style', result, fieldlist);
            if (widget_style != undefined) {
                if (widget_style) {
                    $("#"+widg_ident).attr("style", widget_style);
                    thiswidget.fieldvalues["widget_style"] = widget_style;
                    }
                else {
                    $("#"+widg_ident).removeAttr("style");
                    thiswidget.fieldvalues["widget_style"] = '';
                    }
                }

            // If set_highlight and highlight_class then check if widget
            // class needs to be set
            let highlight_class = thiswidget.fieldvalues["highlight_class"];
            if (highlight_class != undefined) {
                let set_highlight = thiswidget.fieldarg_in_result('set_highlight', result, fieldlist);
                if (set_highlight != undefined){
                    if (set_highlight) {
                        $("#"+widg_ident).attr("class", highlight_class);
                        }
                    else {
                        let stored_widget_class = thiswidget.fieldvalues["widget_class"];
                        if (stored_widget_class){
                            $("#"+widg_ident).attr("class", stored_widget_class);
                            }
                        else {
                            $("#"+widg_ident).removeAttr("class");
                            }
                        }
                     }
                }

            // now call widget method to set any other values
            thiswidget.setvalues(fieldlist, result);
            }
        }
    catch(err) {
         if (SKIPOLE.CatchToHTML) {
             // Calls the URL given by "CatchToHTML"
             window.location.href = SKIPOLE.CatchToHTML + "?ident=" + SKIPOLE.identdata;
             }
         else {
             alert(err.message);
             }
        }
    };

// for an input text widgfield, call its validators
// this is called by widgets that submit a text input field
SKIPOLE.validate = function(widgfield_name, widgfield_value) {
    let widgparts = widgfield_name.split(":");
    let field_no_i = widgparts[1].split("-")[0];
    let name_no_i = widgparts[0] + ":" + field_no_i;
    if (!(name_no_i in SKIPOLE.validators)) {
       return [true, '', ''];
       };
    let val_list = SKIPOLE.validators[name_no_i];
    let count = val_list.length;
    if (count === 0) {
       return [true, '', ''];
       };
    for(let i = 0; i < count; i++) {
       let val = val_list[i];
       let allowed_values = val[3];
       if (!(widgfield_value in allowed_values)) {
           let module = val[0];
           let valclass = val[1];
           let error_message = val[2];
           let args = val[4];
           let validator = SKIPOLE[module][valclass];
           let result = validator(widgfield_value, allowed_values, args);
           let default_error_widget = SKIPOLE.default_error_widget;
           if (!result) {
               if (val[5]) {
                   return [false, error_message, val[5]];
                   }
               else {
                   return [false, error_message, default_error_widget];
                   }
               };
           };
       };
    return [true, '', ''];
    };
// for a form holding multiple input text fields and contained widgets, for each field, call its validators
// return true if ok, false if not.  If false - validation failed, set input_errored_class
// into input fields, and display validation error messages
SKIPOLE.form_validate = function(selected_form) {
    let all_ok = true;
    selected_form.find('input[type="text"], input[type="password"]').each(function() {
        // for each text input field, get its value and call any validator functions
        let text_input = $(this);
        if (text_input.prop('disabled')) {
            return true;
            }
        // get the widget of this input field
        let input_widg_id = text_input.prop('name').split(":")[0];
        if (input_widg_id in SKIPOLE.widgets) {
            var input_widg = SKIPOLE.widgets[input_widg_id];
            }
        else {
            return true;
            }
        // error_status[0] is true if ok, false if not
        // error_status[1] is an optional error message from the widgfield
        // error_status[2] is the validator display widget
        let error_status = SKIPOLE.validate(text_input.prop('name'), text_input.val());
        if (error_status[0]) {
            // validated - remove input_errored_class
            if ("input_errored_class" in input_widg.fieldvalues) {
               text_input.removeClass( input_widg.fieldvalues["input_errored_class"] );
               }
            }
        else {
            // failed validation - add input_errored_class, remove input_accepted_class
            if ("input_errored_class" in input_widg.fieldvalues) {
              text_input.addClass(input_widg.fieldvalues["input_errored_class"]);
              }
            if ("input_accepted_class" in input_widg.fieldvalues) {
               text_input.removeClass(input_widg.fieldvalues["input_accepted_class"]);
               }
            all_ok = false;
            if (error_status[2]) {
                if (error_status[2] in SKIPOLE.widgets) {
                    SKIPOLE.widgets[error_status[2]].show_error(error_status[1]);
                    }
                }
            }
        })
    return all_ok;
    };

// sets <br /> into the string and escapes other html characters
SKIPOLE.textbr = function(string) {
    let entityMap = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': '&quot;',
        "'": '&#39;',
        "/": '&#x2F;',
        "`": '&#x60;',
        "=": '&#x3D;',
       "\n": '<br />'
        };
    return String(string).replace(/[&<>"'`=\/]|[\n]/g, function (s) {
      return entityMap[s];
    });
  };


// Used when a request for a json file fails
SKIPOLE.json_failed = function( jqXHR, textStatus, errorThrown ) {
        let msg = '';
        if (jqXHR.status === 0) {
            msg = 'Connection failure: Possible network problem.';
        } else if (jqXHR.status == 404) {
            msg = '404 : Requested page not found.';
        } else if (jqXHR.status == 500) {
            msg = '500 : Internal Server Error.';
        } else if (textStatus === 'parsererror') {
            msg = 'Unable to parse requested JSON file.';
        } else if (textStatus === 'timeout') {
            msg = 'Request timed out.';
        } else if (textStatus === 'abort') {
            msg = 'Request aborted.';
        } else {
            msg = 'Error: ' + jqXHR.responseText;
        }
        // display the message in the page default_error_widget
       if (SKIPOLE.default_error_widget) {
           // create dictionary result, to be used instead of received json file
           // and flags an error message in the page default error widget
           let result = {};
           result[SKIPOLE.default_error_widget + ":show_error"] = msg;
           SKIPOLE.setfields( result );
       } else {
           alert(msg);
       }
    };


/* base class for widgets */


SKIPOLE.BaseWidget = function (widg_id, error_message, fieldmap) {
    this.widg_id = widg_id;
    this.error_message = error_message;
    this.fieldmap = fieldmap;
    this.fieldvalues = {};
    this.display_errors = true;
    this.widg = $("#"+this.widg_id);
    };


SKIPOLE.BaseWidget.prototype.fieldname = function(fieldarg) {
    if (!this.widg_id) {
        return;
        }
    if (fieldarg in this.fieldmap) {
        return this.fieldmap[fieldarg];
        }
    else {
        return fieldarg;
        }
    };

SKIPOLE.BaseWidget.prototype.formname = function(fieldarg) {
    if (!this.widg_id) {
        return;
        }
    return this.widg_id + ":" + this.fieldname(fieldarg);
    };

SKIPOLE.BaseWidget.prototype.validate = function(fieldarg, fieldval) {
    if (!this.widg_id) {
        return [true, '', ''];
        }
    let widgfield = this.widg_id + ':' + this.fieldname(fieldarg);
    return SKIPOLE.validate(widgfield, fieldval);
    };

SKIPOLE.BaseWidget.prototype.fieldarg_in_result = function (fieldarg, result, fieldlist) {
    let fieldname = this.fieldname(fieldarg);
    if ($.inArray(fieldname, fieldlist) !== -1) {
        let widgfield = this.widg_id + ":" + fieldname;
        if (widgfield in result) {
            return result[widgfield];
            }
        }
    };

SKIPOLE.BaseWidget.prototype.set_attribute = function (attname, fieldarg, result, fieldlist) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    let attval = this.fieldarg_in_result(fieldarg, result, fieldlist);
    if (attval != undefined) {
        if (attval) {
            the_widg.attr(attname, attval);
            }
        else {
            the_widg.removeAttr(attname);
            }
        }
    };

// sets four hidden fields of a form
SKIPOLE.BaseWidget.prototype.sethiddenfields = function(fieldlist, result) {
    // alter hidden_fields in the form, or append new ones if they dont exist
    let formtag = this.widg.find("form");
    if (formtag.length !== 1){
        return;
        }
    // hidden_field1
    let hf1 = this.fieldarg_in_result('hidden_field1', result, fieldlist);
    if (hf1 !== undefined) {
        let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field1') + "\"]";
        let isfield = this.widg.find(find_field_name);
        if (isfield.length){
            isfield.first().val(hf1);
            }
        else {
            let hftagstring = "<input type='hidden' name=\"" + this.formname('hidden_field1') + "\" value=\"" + hf1 +"\">";
            formtag.append(hftagstring);
            }
        }
    // hidden_field2
    let hf2 = this.fieldarg_in_result('hidden_field2', result, fieldlist);
    if (hf2 !== undefined) {
        let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field2') + "\"]";
        let isfield = this.widg.find(find_field_name);
        if (isfield.length){
            isfield.first().val(hf2);
            }
        else {
            let hftagstring = "<input type='hidden' name=\"" + this.formname('hidden_field2') + "\" value=\"" + hf2 +"\">";
            formtag.append(hftagstring);
            }
        }
    // hidden_field3
    let hf3 = this.fieldarg_in_result('hidden_field3', result, fieldlist);
    if (hf3 !== undefined) {
        let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field3') + "\"]";
        let isfield = this.widg.find(find_field_name);
        if (isfield.length){
            isfield.first().val(hf3);
            }
        else {
            let hftagstring = "<input type='hidden' name=\"" + this.formname('hidden_field3') + "\" value=\"" + hf3 +"\">";
            formtag.append(hftagstring);
            }
        }
    // hidden_field4
    let hf4 = this.fieldarg_in_result('hidden_field4', result, fieldlist);
    if (hf4 !== undefined) {
        let find_field_name = "input:hidden[name=\"" + this.formname('hidden_field4') + "\"]";
        let isfield = this.widg.find(find_field_name);
        if (isfield.length){
            isfield.first().val(hf4);
            }
        else {
            let hftagstring = "<input type='hidden' name=\"" + this.formname('hidden_field4') + "\" value=\"" + hf4 +"\">";
            formtag.append(hftagstring);
            }
        }
    };

// given href, and a get field with new value, returns new href with changed get field
SKIPOLE.BaseWidget.prototype.setgetfield = function(href, fieldarg, fieldvalue) {
    let get_field_value =  encodeURIComponent( fieldvalue );
    let get_field_name = this.formname(fieldarg);
    // fieldname may have : so when comparing with href parts, need encoded value
    let encode_field_name = encodeURIComponent( get_field_name );
    let qindex = href.indexOf('?');
    if (qindex === -1) {
        if ( get_field_value === '') {
            return href;
            }
        else {
            return href + "?ident=" + SKIPOLE.identdata + "&" + get_field_name + "=" + get_field_value;
            }
        }
    let url = href.substring(0, qindex);
    let querystring = href.substring(qindex+1);
    let ampindex = querystring.indexOf('&');
    if (ampindex === -1) {
        let qv = querystring.split('=');
        if ((qv[0] === encode_field_name) || (qv[0] === get_field_name)) {
            if ( get_field_value === '') {
                return url;
                }
            else {
                return url + "?" + get_field_name + "=" + get_field_value;
                }
            }
        else {
            if ( get_field_value === '') {
                return href;
                }
            else {
                return href + "&" + get_field_name + "=" + get_field_value;
                }
             }
        }
    let queries = querystring.split("&");
    let qlist = [];
    let flag = false;
    for (let index = 0; index < queries.length; ++index) {
        let qv = queries[index].split('=');
        if ((qv[0] === encode_field_name) || (qv[0] === get_field_name)) {
            qv[1] = get_field_value;
            flag = true;
            }
        if (qv[1] !== '') {
            qlist.push( qv[0] + '=' + qv[1] );
            }
        };
    if (!flag) {
        if (get_field_value !== '') {
            qlist.push( get_field_name + "=" + get_field_value);
            }
        }
    let new_query = qlist.join("&");
    return url + "?" + new_query;
  };


SKIPOLE.BaseWidget.prototype.get_error = function (result) {
    if (!this.display_errors) {
        return;
        }
    let fieldname = this.fieldname('show_error');
    let widgfield = this.widg_id + ":" + fieldname;
    if (!(widgfield in result)) {
        widgfield = this.widg_id + ":show_error";
        if (!(widgfield in result)) {
            return;
            }
        }
    if (result[widgfield]) {
        return result[widgfield];
        }
    if (this.error_message) {
        return this.error_message;
        }
    return "Unknown Error";
    };


SKIPOLE.BaseWidget.prototype.check_error = function (fieldlist, result) {
    /* show error if an error message is given, clear error if clear_error is given */
    /* return true on error, false otherwise */
    if (!this.display_errors) {
        return false;
        }
    let error_message = this.get_error(result);
    if (error_message) {
        this.show_error(error_message);
        return true;
        }
    // check for clear_error
    let clear = this.fieldarg_in_result('clear_error', result, fieldlist);
    if (clear) {
        this.clear_error();
        }
    return false;
    };


SKIPOLE.BaseWidget.prototype.setvalues = function (fieldlist, result) {
    /* accept show_error */
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    };

SKIPOLE.BaseWidget.prototype.set_accepted = function (input_field, input_accepted) {
    // input_accepted
    if ((input_accepted === true) || (input_accepted === "True")) {
            if ("input_accepted_class" in this.fieldvalues) {
               input_field.addClass(this.fieldvalues["input_accepted_class"]);
               }
            if ("input_errored_class" in this.fieldvalues) {
               input_field.removeClass( this.fieldvalues["input_errored_class"] );
               }
        }
   if ((input_accepted === false) || (input_accepted === "False")) {
            if ("input_accepted_class" in this.fieldvalues) {
               input_field.removeClass( this.fieldvalues["input_accepted_class"] );
               }
        }
    };

SKIPOLE.BaseWidget.prototype.set_errored = function (input_field, input_errored) {
    // input_errored
    if ((input_errored === true) || (input_errored === "True")) {
            if ("input_errored_class" in this.fieldvalues) {
               input_field.addClass(this.fieldvalues["input_errored_class"]);
               }
            if ("input_accepted_class" in this.fieldvalues) {
               input_field.removeClass( this.fieldvalues["input_accepted_class"] );
               }
        }
   if ((input_errored === false) || (input_errored === "False")) {
            if ("input_errored_class" in this.fieldvalues) {
               input_field.removeClass( this.fieldvalues["input_errored_class"] );
               }
        }
    };

SKIPOLE.BaseWidget.prototype.set_accepted_errored = function (input_field, fieldlist, result) {
    // input_accepted
    let input_accepted = this.fieldarg_in_result('set_input_accepted', result, fieldlist);
    this.set_accepted(input_field, input_accepted);
    // input_errored
    let input_errored = this.fieldarg_in_result('set_input_errored', result, fieldlist);
    this.set_errored(input_field, input_errored);
    };

SKIPOLE.BaseWidget.prototype.set_if_disabled = function (input_field, input_disabled, fieldlist, result) {
    if ((input_disabled === true) || (input_disabled === "True")) {
            if ("input_disabled_class" in this.fieldvalues) {
                if ("input_class" in this.fieldvalues) {
                   input_field.removeClass( this.fieldvalues["input_class"] );
                   }
               input_field.addClass(this.fieldvalues["input_disabled_class"]);
               }
            input_field.attr("disabled", "disabled");
        }
    if ((input_disabled === false) || (input_disabled === "False")) {
            if ("input_disabled_class" in this.fieldvalues) {
               input_field.removeClass( this.fieldvalues["input_disabled_class"] );
                if ("input_class" in this.fieldvalues) {
                   input_field.addClass(this.fieldvalues["input_class"]);
                   }
               }
            input_field.removeAttr("disabled");
        }
    };

SKIPOLE.BaseWidget.prototype.show_error = function (error_message) {
    /* prototype sets data-status and ensures first paragraph contains error_message and is visible  */
    if (!this.display_errors) {
        return;
        }
    if (!error_message) {
        error_message = this.error_message;
        }
    if (!error_message) {
        error_message = "Unknown Error";
        }
    let the_widg = this.widg;
    the_widg.attr("data-status", "error");
    // get error div, being first child
    let error_div = the_widg.find(':first');
    let error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };

SKIPOLE.BaseWidget.prototype.clear_error = function() {
    /* prototype clears data-status and ensures first paragraph is hidden  */
    if (!this.display_errors) {
        return;
        }
    let the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" );
        }
    let error_div = the_widg.find(':first');
    if (error_div.is(":visible")) {
        error_div.hide();
        }
    };


// clear errors on the page
SKIPOLE.clear_all_errors = function() {
    $('[data-status="error"]').each(function() {
        // for each widget
        let thiselement = $(this);
        // get the widget of this thiselement
        let widg_id = thiselement.prop('id');
        if (widg_id in SKIPOLE.widgets) {
            let this_widg = SKIPOLE.widgets[widg_id];
            this_widg.clear_error();
            }
    })
}
