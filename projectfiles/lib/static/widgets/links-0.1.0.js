/*
####### SKIPOLE WEB FRAMEWORK #######

 links-0.1.0.js  - javascript widgets

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


SKIPOLE.links = {};

SKIPOLE.links.Link = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.Link.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.Link.prototype.constructor = SKIPOLE.links.Link;
SKIPOLE.links.Link.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    // content
    var content = this.fieldarg_in_result('content', result, fieldlist);
    if (content) {
        this.widg.text(content);
        }
    };


SKIPOLE.links.ImageOrTextLink = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.ImageOrTextLink.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.ImageOrTextLink.prototype.constructor = SKIPOLE.links.ImageOrTextLink;


SKIPOLE.links.JSONButtonLink = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.links.JSONButtonLink.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.JSONButtonLink.prototype.constructor = SKIPOLE.links.JSONButtonLink;
SKIPOLE.links.JSONButtonLink.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    // set the widget class to widget_class
    var widget_class = this.fieldarg_in_result('widget_class', result, fieldlist);
    if (widget_class) {
        the_widg.attr('class', widget_class);
        }
    };
SKIPOLE.links.JSONButtonLink.prototype.show_error = function (error_message) {
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
    the_widg.text(error_message);
    // set the widget class to error class
    var error_class = this.fieldarg_in_result('error_class', result, fieldlist);
    if (error_class) {
        the_widg.attr('class', error_class);
        }
    if (!(the_widg.is(":visible"))) {
         the_widg.fadeIn('slow');
        }
    };
SKIPOLE.links.JSONButtonLink.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    /* check if an error message or clear_error is given */
    if (this.check_error(fieldlist, result)) {
        return;
        }
    var button_text = this.fieldarg_in_result('button_text', result, fieldlist);
    if (button_text) {
        the_widg.text(button_text);
        }
    var href = the_widg.attr('href');
    /* get_field1 */
    var get_field1 = this.fieldarg_in_result('get_field1', result, fieldlist);
    if (get_field1 != undefined) {
        var href = the_widg.attr('href');
        var url = this.setgetfield(href, 'get_field1', get_field1);
        the_widg.attr('href', url);
        }
    /* get_field2 */
    var get_field2 = this.fieldarg_in_result('get_field2', result, fieldlist);
    if (get_field2 != undefined) {
        var href = the_widg.attr('href');
        var url = this.setgetfield(href, 'get_field2', get_field2);
        the_widg.attr('href', url);
        }
    /* hide */
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
SKIPOLE.links.JSONButtonLink.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    if (!fieldvalues["url"]) {
        return;
        }
    var the_widg = this.widg;
    var href = the_widg.attr('href');
    var senddata = href.substring(href.indexOf('?')+1);
    var buttontext = the_widg.text();
    var button_wait_text = fieldvalues["button_wait_text"]
    the_widg.text(button_wait_text);
    $.getJSON(fieldvalues["url"], senddata)
        .done(function(result){
            SKIPOLE.setfields(result);
            })
        .always(function() {
            if (the_widg.text() == button_wait_text) {
                the_widg.text(buttontext);
                }
            });
    e.preventDefault();
    };


SKIPOLE.links.ButtonLink1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.links.ButtonLink1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.ButtonLink1.prototype.constructor = SKIPOLE.links.ButtonLink1;
SKIPOLE.links.ButtonLink1.prototype.clear_error = function () {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    the_widg.removeAttr("data-status");
    // set the widget class to widget_class
    var widget_class = this.fieldarg_in_result('widget_class', result, fieldlist);
    if (widget_class) {
        the_widg.attr('class', widget_class);
        }
    };
SKIPOLE.links.ButtonLink1.prototype.show_error = function (error_message) {
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
    the_widg.text(error_message);
    // set the widget class to error class
    var error_class = this.fieldarg_in_result('error_class', result, fieldlist);
    if (error_class) {
        the_widg.attr('class', error_class);
        }
    if (!(the_widg.is(":visible"))) {
         the_widg.fadeIn('slow');
        }
    };
SKIPOLE.links.ButtonLink1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    /* check if an error message or clear_error is given */
    if (this.check_error(fieldlist, result)) {
        return;
        }
    var button_text = this.fieldarg_in_result('button_text', result, fieldlist);
    if (button_text) {
        the_widg.text(button_text);
        }
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


SKIPOLE.links.ButtonLink2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.links.ButtonLink2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.ButtonLink2.prototype.constructor = SKIPOLE.links.ButtonLink2;
SKIPOLE.links.ButtonLink2.prototype.show_error = function (error_message) {
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
    // if widg not visible, show it
    if (!(the_widg.is(":visible"))) {
         the_widg.show();
        }
    // get error div, being first child
    var error_div = the_widg.find(':first');
    var error_para = error_div.find(':first');
    error_para.text(error_message);
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };
SKIPOLE.links.ButtonLink2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    var button_text = this.fieldarg_in_result('button_text', result, fieldlist);
    var a_link = the_widg.find('a');
    if (button_text) {
        a_link.text(button_text);
        }
    /* check if an error message or clear_error is given */
    if (this.check_error(fieldlist, result)) {
        return;
        }
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
SKIPOLE.links.ButtonLink2.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    var the_widg = this.widg;
    // set button_wait_text
    var a_link = the_widg.find('a');
    var href = a_link.attr('href');
    var buttontext = a_link.text();
    var button_wait_text = fieldvalues["button_wait_text"]
    if (button_wait_text) {
        a_link.text(button_wait_text);
        }
    if (!fieldvalues["url"]) {
        // no json url, return and call html link
        return;
        }
    var senddata = href.substring(href.indexOf('?')+1);
    $.getJSON(fieldvalues["url"], senddata)
        .done(function(result){
            SKIPOLE.setfields(result);
            })
        .always(function() {
            if (a_link.text() == button_wait_text) {
                a_link.text(buttontext);
                }
            });
    e.preventDefault();
    };


SKIPOLE.links.CloseButton = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.CloseButton.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.CloseButton.prototype.constructor = SKIPOLE.links.CloseButton;
SKIPOLE.links.CloseButton.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    var the_widg = this.widg;
    // get id of target
    var target_section = fieldvalues["target_section"];
    var target_widget = fieldvalues["target_widget"];
    if (target_section && target_widget) {
        var target_id = target_section + "-" + target_widget;
    } else if ( target_section ) {
        var target_id = target_section;
    } else if ( target_widget ) {
        var target_id = target_widget;
    } else {
        var target_id = "";
    }

    if (!target_id) {
        return;
        }
    // close item with target_id
    var target = $("#"+target_id);
    if (target) {
        if (target.is(":visible")) {
            target.hide();
            }
        e.preventDefault();
        }
    };


SKIPOLE.links.OpenButton = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.OpenButton.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.OpenButton.prototype.constructor = SKIPOLE.links.OpenButton;
SKIPOLE.links.OpenButton.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    var the_widg = this.widg;
    // get id of target
    var target_section = fieldvalues["target_section"];
    var target_widget = fieldvalues["target_widget"];
    if (target_section && target_widget) {
        var target_id = target_section + "-" + target_widget;
    } else if ( target_section ) {
        var target_id = target_section;
    } else if ( target_widget ) {
        var target_id = target_widget;
    } else {
        var target_id = "";
    }

    if (!target_id) {
        return;
        }
    // open item with target_id
    var target = $("#"+target_id);
    if (target) {
        if (!(target.is(":visible"))) {
            target.show();
            }
        e.preventDefault();
        }
    };


SKIPOLE.links.ImageLink1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.ImageLink1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.ImageLink1.prototype.constructor = SKIPOLE.links.ImageLink1;


SKIPOLE.links.CSSLink = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.CSSLink.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.CSSLink.prototype.constructor = SKIPOLE.links.CSSLink;


SKIPOLE.links.FaviconLink = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.FaviconLink.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.FaviconLink.prototype.constructor = SKIPOLE.links.FaviconLink;


SKIPOLE.links.ScriptLink = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.ScriptLink.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.ScriptLink.prototype.constructor = SKIPOLE.links.ScriptLink;


SKIPOLE.links.LinkTextBlockTable1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.LinkTextBlockTable1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.LinkTextBlockTable1.prototype.constructor = SKIPOLE.links.LinkTextBlockTable1;


SKIPOLE.links.LinkTextBlockTable2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.LinkTextBlockTable2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.LinkTextBlockTable2.prototype.constructor = SKIPOLE.links.LinkTextBlockTable2;

SKIPOLE.links.ListLinks = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.ListLinks.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.ListLinks.prototype.constructor = SKIPOLE.links.ListLinks;

SKIPOLE.links.Table1_Button = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.Table1_Button.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.Table1_Button.prototype.constructor = SKIPOLE.links.Table1_Button;
SKIPOLE.links.Table1_Button.prototype.setvalues = function (fieldlist, result) {
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
SKIPOLE.links.Table1_Button.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    if (!fieldvalues["url"]) {
        return;
        }
    var href = $(e.target).attr('href');
    var senddata = href.substring(href.indexOf('?')+1);
    $.getJSON(fieldvalues["url"], senddata)
        .done(function(result){
            SKIPOLE.setfields(result);
            });
    e.preventDefault();
    };



SKIPOLE.links.Table2_Button = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.Table2_Button.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.Table2_Button.prototype.constructor = SKIPOLE.links.Table2_Button;
SKIPOLE.links.Table2_Button.prototype.setvalues = function (fieldlist, result) {
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
SKIPOLE.links.Table2_Button.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    if (!fieldvalues["url"]) {
        return;
        }
    var href = $(e.target).attr('href');
    var senddata = href.substring(href.indexOf('?')+1);
    $.getJSON(fieldvalues["url"], senddata)
        .done(function(result){
            SKIPOLE.setfields(result);
            });
    e.preventDefault();
    };


SKIPOLE.links.Table3_Buttons2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.Table3_Buttons2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.Table3_Buttons2.prototype.constructor = SKIPOLE.links.Table3_Buttons2;
SKIPOLE.links.Table3_Buttons2.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    var button = $(e.target);
    var myCol = button.parent().index();
    var href = button.attr('href');
    if (!href) {
        return;
        }
    var senddata = href.substring(href.indexOf('?')+1);

    if (myCol === 3) {
        if (!fieldvalues["url1"]) {
            return;
            }
        $.getJSON(fieldvalues["url1"], senddata)
            .done(function(result){
                SKIPOLE.setfields(result);
                });
        } else if (myCol === 4) {
            if (!fieldvalues["url2"]) {
                return;
                }
            $.getJSON(fieldvalues["url2"], senddata)
                .done(function(result){
                SKIPOLE.setfields(result);
                });
        } else {
            return;
        }
    e.preventDefault();
    };


SKIPOLE.links.Table1_Buttons4 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.Table1_Buttons4.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.Table1_Buttons4.prototype.constructor = SKIPOLE.links.Table1_Buttons4;


SKIPOLE.links.GeneralButtonTable1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.GeneralButtonTable1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.GeneralButtonTable1.prototype.constructor = SKIPOLE.links.GeneralButtonTable1;
SKIPOLE.links.GeneralButtonTable1.prototype.setvalues = function (fieldlist, result) {
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


SKIPOLE.links.GeneralButtonTable2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.links.GeneralButtonTable2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.links.GeneralButtonTable2.prototype.constructor = SKIPOLE.links.GeneralButtonTable2;
SKIPOLE.links.GeneralButtonTable2.prototype.eventfunc = function (e) {
    if (!this.widg_id) {
        return;
        }
    var fieldvalues = this.fieldvalues;
    var button = $(e.target);
    var href = button.attr('href');
    if (!href) {
        return;
        }
    if (!fieldvalues["json_url"]) {
        return;
        }
    var senddata = href.substring(href.indexOf('?')+1);
    /* fieldvalues["json_url"] is a list of column json urls
       need to get the column index to find which of these
       urls to send the call to */
    var col = button.parent().index();
    if (!fieldvalues["json_url"][col]) {
        return;
        }
    $.getJSON(fieldvalues["json_url"][col], senddata)
        .done(function(result){
            SKIPOLE.setfields(result);
            });
    e.preventDefault();
    };

SKIPOLE.links.GeneralButtonTable2.prototype.dragstartfunc = function (e, data) {
    e.dataTransfer.setData("text/widgid", this.widg_id);
    e.dataTransfer.setData("text/plain", data);
    };
SKIPOLE.links.GeneralButtonTable2.prototype.dropfunc = function (e, data) {
    e.preventDefault();
    var widg_id = e.dataTransfer.getData("text/widgid");
    if (widg_id != this.widg_id) {
        return;
        }
    var url = this.fieldvalues["dropurl"];
    if (!url) {
        return;
        }
    // now make a call, including data from the drag element and the drop element
    var dragwidgfield = this.formname('dragrows');
    var dropwidgfield = this.formname('droprows');

    var senddata = "ident=" + SKIPOLE.identdata;
    if (data) {
        senddata = senddata + "&" + dropwidgfield + "=" + data;
        }
    if (e.dataTransfer.getData("text/plain")) {
        senddata = senddata + "&" + dragwidgfield + "=" + e.dataTransfer.getData("text/plain");
        }
    $.getJSON(url, senddata)
        .done(function(result){
            SKIPOLE.setfields(result);
            });
    };
SKIPOLE.links.GeneralButtonTable2.prototype.allowdropfunc = function (e) {
     e.preventDefault();
    };

SKIPOLE.links.GeneralButtonTable2.prototype.setvalues = function (fieldlist, result) {
   if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    var fieldvalues = this.fieldvalues;
    // hide the widget
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
    // the class of the button's if any
    var button_class = fieldvalues["button_class"];
    // get column urls and number of columns
    var json_url = fieldvalues["json_url"];
    var html_url = fieldvalues["html_url"];
    if (json_url == undefined) {
        return;
        }
    if (html_url == undefined) {
        return;
        }
    var cols = html_url.length;
    if (cols != json_url.length) {
        return;
        }
    // cols is the number of columns

    // The table contents
    var contents = this.fieldarg_in_result('contents', result, fieldlist);
    if (!contents) {
        return;
        }
    var rows = Math.floor(contents.length/cols);
    if (rows*cols != contents.length) {
        return;
        }
    // empty the table
    the_widg.empty();
    // and now start filling it again
    var htmlcontent = "";
    var cell = -1;
    for (row = 0; row < rows; row++) {
        htmlcontent += "<tr>";
        // row content to be added here


        for (col = 0; col < cols; col++) {
            cell += 1;
            var element = contents[cell];
            // cell text
            var celltext = '';
            if (element[0]) {
                celltext = element[0];
                }
            // cell style
            if (element[1]) {
                htmlcontent += "<td " + "style = \"" + element[1] + "\">";
                }
            else {
                htmlcontent += "<td>";
                }
            // get html url for this column
            var url = html_url[col];
            // is it a button link
            if (url && element[2]) {
                // its a link, apply button class
                if (button_class) {
                    htmlcontent +=  "<a role = \"button\" class = \"" + button_class + "\"";
                    }
                else {
                    htmlcontent +=  "<a role = \"button\"";
                    }
                // get url and create href attribute
                if (element[3]) {
                    url += "?ident=" + SKIPOLE.identdata + "&" + this.formname("contents") + "=" + element[3];
                    }
                else {
                    url += "?ident=" + SKIPOLE.identdata
                    }
                htmlcontent +=  " href = \"" + url + "\">";
                // apply button text and close <a> tag
                if (celltext) {
                    htmlcontent += celltext + "</a>";
                    }
                else {
                    htmlcontent += url + "</a>";
                    }
                }
            else {
                // not a link
                htmlcontent += celltext;
                }

            htmlcontent += "</td>";
            }
        htmlcontent += "</tr>";
        }
    the_widg.html(htmlcontent);
    };


