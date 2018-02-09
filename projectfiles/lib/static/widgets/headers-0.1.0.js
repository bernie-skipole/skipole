/*
####### SKIPOLE WEB FRAMEWORK #######

 headers-0.1.0.js  - javascript widgets

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


SKIPOLE.headers = {};


SKIPOLE.headers.HeaderErrorPara = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderErrorPara.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderErrorPara.prototype.constructor = SKIPOLE.headers.HeaderErrorPara;
SKIPOLE.headers.HeaderErrorPara.prototype.setvalues = function (fieldlist, result) {
    /* accept show_error */
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    /*  if hide is given */
    var the_widg = this.widg;
    // hide
    var hidebox = this.fieldarg_in_result('hide', result, fieldlist);
    if (hidebox != undefined) {
        if (hidebox) {
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
SKIPOLE.headers.HeaderErrorPara.prototype.show_error = function (error_message) {
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
    if (!(the_widg.is(":visible"))) {
        the_widg.text(error_message).fadeIn('slow');
        }
    };
SKIPOLE.headers.HeaderErrorPara.prototype.clear_error = function() {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    if (the_widg.is(":visible")) {
        the_widg.fadeOut('slow');
        }
    };


SKIPOLE.headers.HeadText = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.headers.HeadText.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeadText.prototype.constructor = SKIPOLE.headers.HeadText;
SKIPOLE.headers.HeadText.prototype.setvalues = function (fieldlist, result) {
    /* This widget accepts field - large_text */
   if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    /* large_text */
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        the_widg.text(large_text);
        }
    };



SKIPOLE.headers.HeaderText1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderText1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderText1.prototype.constructor = SKIPOLE.headers.HeaderText1;
SKIPOLE.headers.HeaderText1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // large_text
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        var h1_text = the_widg.find('h2');
        h1_text.text(large_text);
        }
    // small_text
    var small_text = this.fieldarg_in_result('small_text', result, fieldlist);
    if (small_text) {
        var p_text = the_widg.find(':nth-child(2)');
        p_text.text(small_text);
        }
    };
SKIPOLE.headers.HeaderText1.prototype.show_error = function (error_message) {
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

    var error_div = the_widg.find(':nth-child(3)');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.headers.HeaderText1.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    var error_div = the_widg.find(':nth-child(3)');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };


SKIPOLE.headers.HeaderText2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderText2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderText2.prototype.constructor = SKIPOLE.headers.HeaderText2;
SKIPOLE.headers.HeaderText2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // large_text
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        var h1_text = the_widg.find('h2');
        h1_text.text(large_text);
        }
    // small_text
    var small_text = this.fieldarg_in_result('small_text', result, fieldlist);
    if (small_text) {
        var p_text = the_widg.find(':nth-child(2)');
        p_text.text(small_text);
        }
    };
SKIPOLE.headers.HeaderText2.prototype.show_error = function (error_message) {
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

    var error_div = the_widg.find(':nth-child(3)');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.headers.HeaderText2.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    var error_div = the_widg.find(':nth-child(3)');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };


SKIPOLE.headers.HeaderText3 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderText3.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderText3.prototype.constructor = SKIPOLE.headers.HeaderText3;
SKIPOLE.headers.HeaderText3.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // large_text
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        var h1_text = the_widg.find('h2');
        h1_text.text(large_text);
        }
    // small_text
    var small_text = this.fieldarg_in_result('small_text', result, fieldlist);
    if (small_text) {
        var p_text = the_widg.find(':nth-child(2)');
        p_text.text(small_text);
        }
    };
SKIPOLE.headers.HeaderText3.prototype.show_error = function (error_message) {
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

    var error_div = the_widg.find(':nth-child(3)');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.headers.HeaderText3.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    var error_div = the_widg.find(':nth-child(3)');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };


SKIPOLE.headers.HeaderText4 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderText4.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderText4.prototype.constructor = SKIPOLE.headers.HeaderText4;
SKIPOLE.headers.HeaderText4.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // large_text
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        var h1_text = the_widg.find('h2');
        h1_text.text(large_text);
        }
    // small_text
    var small_text = this.fieldarg_in_result('small_text', result, fieldlist);
    if (small_text) {
        var p_text = the_widg.find(':nth-child(2)');
        p_text.text(small_text);
        }
    };
SKIPOLE.headers.HeaderText4.prototype.show_error = function (error_message) {
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

    var error_div = the_widg.find(':nth-child(3)');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.headers.HeaderText4.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    var error_div = the_widg.find(':nth-child(3)');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };

SKIPOLE.headers.HeaderText5 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderText5.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderText5.prototype.constructor = SKIPOLE.headers.HeaderText5;
SKIPOLE.headers.HeaderText5.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // large_text
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        var h1_text = the_widg.find('h2');
        h1_text.text(large_text);
        }
    // small_text
    var small_text = this.fieldarg_in_result('small_text', result, fieldlist);
    if (small_text) {
        var p_text = the_widg.find(':nth-child(2)');
        p_text.text(small_text);
        }
    };
SKIPOLE.headers.HeaderText5.prototype.show_error = function (error_message) {
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

    var error_div = the_widg.find(':nth-child(3)');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.headers.HeaderText5.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    var error_div = the_widg.find(':nth-child(3)');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };


SKIPOLE.headers.HeaderText6 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.HeaderText6.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.HeaderText6.prototype.constructor = SKIPOLE.headers.HeaderText6;
SKIPOLE.headers.HeaderText6.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    var the_widg = this.widg;
    // large_text
    var large_text = this.fieldarg_in_result('large_text', result, fieldlist);
    if (large_text) {
        var h1_text = the_widg.find('h2');
        h1_text.text(large_text);
        }
    // small_text
    var small_text = this.fieldarg_in_result('small_text', result, fieldlist);
    if (small_text) {
        var p_text = the_widg.find(':nth-child(2)');
        p_text.text(small_text);
        }
    };
SKIPOLE.headers.HeaderText6.prototype.show_error = function (error_message) {
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

    var error_div = the_widg.find(':nth-child(3)');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.headers.HeaderText6.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    var error_div = the_widg.find(':nth-child(3)');
    if (error_div.is(":visible")) {
        //error_div.fadeOut('slow');
        error_div.hide();
        }
    };

SKIPOLE.headers.NavButtons1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.headers.NavButtons1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.NavButtons1.prototype.constructor = SKIPOLE.headers.NavButtons1;


SKIPOLE.headers.NavButtons2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.headers.NavButtons2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.NavButtons2.prototype.constructor = SKIPOLE.headers.NavButtons2;


SKIPOLE.headers.TabButtons1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.headers.TabButtons1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.headers.TabButtons1.prototype.constructor = SKIPOLE.headers.TabButtons1;
SKIPOLE.headers.TabButtons1.prototype.eventfunc = function (e) {
    var button = $(e.target);
    this.setbutton(button.index());
    }
SKIPOLE.headers.TabButtons1.prototype.setbutton = function (button_index) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    var the_widg = this.widg;
    var allbuttons = the_widg.find('button');
    var button = allbuttons.eq(button_index);
    if (fieldvalues["onclick_removeclass"]){
        // add the class to all buttons
        allbuttons.addClass( fieldvalues["onclick_removeclass"] );
        // remove this class from the pressed button
        button.removeClass( fieldvalues["onclick_removeclass"] );
        }
    if (fieldvalues["onclick_addclass"]){
        // remove the class from all buttons
        allbuttons.removeClass( fieldvalues["onclick_addclass"] );
        // add this class to the pressed button
        button.addClass( fieldvalues["onclick_addclass"] );
        }
    var displayid = fieldvalues["display_id_list"][button_index];
    // hide all items with hide_class
    if (fieldvalues["hide_class"]) {
        $("." + fieldvalues["hide_class"]).hide();
        }
    // display the item with the given id
    if (displayid) {
        $("#" + displayid).show();
        }
    }



