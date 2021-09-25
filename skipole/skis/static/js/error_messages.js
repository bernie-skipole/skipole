


SKIPOLE.error_messages = {};

SKIPOLE.error_messages.ErrorCode = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.error_messages.ErrorCode.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.error_messages.ErrorCode.prototype.constructor = SKIPOLE.error_messages.ErrorCode;
SKIPOLE.error_messages.ErrorCode.prototype.setvalues = function (fieldlist, result) {
    /* This widget accepts fields - para_text */
   if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    if (this.check_error(fieldlist, result)) {
        return;
        }
    let para_text = this.fieldarg_in_result('para_text', result, fieldlist);
    if (para_text) {
        let paragraph = this.widg.find(':first').next();
        paragraph.text(para_text);
        }
    };
SKIPOLE.error_messages.ErrorCode.prototype.show_error = function (error_message) {
    /* sets data-status and ensures first child contains error_message and has class error_class  */
    if (!error_message) {
        error_message = this.error_message;
        }
    if (!error_message) {
        error_message = "Unknown Error";
        }
    let the_widg = this.widg;
    the_widg.attr("data-status", "error");
    let paragraph = the_widg.find(':first').next();
    paragraph.text(error_message);
    let error_class = this.fieldvalues["error_class"];
    if (error_class) {
        paragraph.attr("class", error_class);
        }
    };
SKIPOLE.error_messages.ErrorCode.prototype.clear_error = function() {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" );
        }
    let paragraph = the_widg.find(':first').next();
    paragraph.removeAttr( "class" );
    let para_class = this.fieldvalues["para_class"];
    if (para_class) {
        paragraph.attr("class", para_class);
        }
    };



SKIPOLE.error_messages.ErrorDiv = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.error_messages.ErrorDiv.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.error_messages.ErrorDiv.prototype.constructor = SKIPOLE.error_messages.ErrorDiv;
SKIPOLE.error_messages.ErrorDiv.prototype.setvalues = function (fieldlist, result) {
    /* accept show_error */
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    /*  if hide is given */
    let the_widg = this.widg;
    // hide
    let hidebox = this.fieldarg_in_result('hide', result, fieldlist);
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
SKIPOLE.error_messages.ErrorDiv.prototype.show_error = function (error_message) {
    if (!this.widg_id) {
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
    if (!(the_widg.is(":visible"))) {
        the_widg.show();
        }
    if (!(error_div.is(":visible"))) {
       error_div.show();
        }
    };



SKIPOLE.error_messages.ErrorPara = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.error_messages.ErrorPara.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.error_messages.ErrorPara.prototype.constructor = SKIPOLE.error_messages.ErrorPara;
SKIPOLE.error_messages.ErrorPara.prototype.setvalues = function (fieldlist, result) {
    /* accept show_error */
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    /*  if hide is given */
    let the_widg = this.widg;
    // hide
    let hidebox = this.fieldarg_in_result('hide', result, fieldlist);
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
SKIPOLE.error_messages.ErrorPara.prototype.show_error = function (error_message) {
    if (!this.widg_id) {
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
    the_widg.text(error_message);
    if (!(the_widg.is(":visible"))) {
        the_widg.fadeIn('slow');
        }
    };
SKIPOLE.error_messages.ErrorPara.prototype.clear_error = function() {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    if (the_widg.is(":visible")) {
        the_widg.fadeOut('slow');
        }
    };


SKIPOLE.error_messages.ErrorClear1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.error_messages.ErrorClear1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.error_messages.ErrorClear1.prototype.constructor = SKIPOLE.error_messages.ErrorClear1;
SKIPOLE.error_messages.ErrorClear1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    let is_error = this.check_error(fieldlist, result);
    let the_widg = this.widg;
    if (!is_error) {
        // if no error condition check hide and para_text
        let para_text = this.fieldarg_in_result('para_text', result, fieldlist);
        if (para_text != undefined) {
            let paragraph = the_widg.find("p:last");
            paragraph.text(para_text);
            }
        let hidebox = this.fieldarg_in_result('hide', result, fieldlist);
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
        }
    let button = the_widg.find("a");
    // get_field1
    let get_field1 = this.fieldarg_in_result('get_field1', result, fieldlist);
    if (get_field1 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field1", get_field1);
        button.attr('href', url);
        }
    // get_field2
    let get_field2 = this.fieldarg_in_result('get_field2', result, fieldlist);
    if (get_field2 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field2", get_field2);
        button.attr('href', url);
        }
    // get_field3
    let get_field3 = this.fieldarg_in_result('get_field3', result, fieldlist);
    if (get_field3 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field3", get_field3);
        button.attr('href', url);
        }
    };
SKIPOLE.error_messages.ErrorClear1.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    the_widg.fadeOut('slow');
    e.preventDefault();
    };
SKIPOLE.error_messages.ErrorClear1.prototype.show_error = function (error_message) {
    if (!this.widg_id) {
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
    // get error para to insert error message
    let paragraph = the_widg.find("p:last");
    paragraph.text(error_message);
    if (!(the_widg.is(":visible"))) {
        the_widg.fadeIn('slow');
        }
    };
SKIPOLE.error_messages.ErrorClear1.prototype.clear_error = function() {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    if (the_widg.is(":visible")) {
        the_widg.fadeOut('slow');
        }
    };


SKIPOLE.error_messages.ErrorClear2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.error_messages.ErrorClear2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.error_messages.ErrorClear2.prototype.constructor = SKIPOLE.error_messages.ErrorClear2;
SKIPOLE.error_messages.ErrorClear2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    let is_error = this.check_error(fieldlist, result);
    let the_widg = this.widg;
    if (!is_error) {
        // if no error condition check hide
        let hidebox = this.fieldarg_in_result('hide', result, fieldlist);
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
        }
    let button = the_widg.find("a");
    // get_field1
    let get_field1 = this.fieldarg_in_result('get_field1', result, fieldlist);
    if (get_field1 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field1", get_field1);
        button.attr('href', url);
        }
    // get_field2
    let get_field2 = this.fieldarg_in_result('get_field2', result, fieldlist);
    if (get_field2 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field2", get_field2);
        button.attr('href', url);
        }
    // get_field3
    let get_field3 = this.fieldarg_in_result('get_field3', result, fieldlist);
    if (get_field3 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field3", get_field3);
        button.attr('href', url);
        }
    };
SKIPOLE.error_messages.ErrorClear2.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    // pressing close is the equivalent of clearing the error
    // and preventing the link send
    this.clear_error();
    e.preventDefault();
    };
SKIPOLE.error_messages.ErrorClear2.prototype.show_error = function (error_message) {
    if (!this.widg_id) {
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
    let fieldvalues = this.fieldvalues;
    // get error para to insert error message
    if (fieldvalues["para_id"]) {
        let para = $('#' + fieldvalues["para_id"]);
        para.text(error_message);
        if (!(the_widg.is(":visible"))) {
            the_widg.fadeIn('slow');
            }
        }
    };
SKIPOLE.error_messages.ErrorClear2.prototype.clear_error = function() {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    if (the_widg.is(":visible")) {
        the_widg.fadeOut('slow');
        }
    };


