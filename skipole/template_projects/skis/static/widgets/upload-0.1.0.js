

SKIPOLE.upload = {};


SKIPOLE.upload.SubmitUploadFile1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.upload.SubmitUploadFile1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.upload.SubmitUploadFile1.prototype.constructor = SKIPOLE.upload.SubmitUploadFile1;
SKIPOLE.upload.SubmitUploadFile1.prototype.setvalues = function (fieldlist, result) {
    /* This widget accepts fields - hide */
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;

    /* for each hidden field div, update the hidden field value if given */

    var val1 = this.fieldarg_in_result('hidden_field1', result, fieldlist);
    if (val1 !== undefined) {
        /* find the div containing the field */
        var div1 = $("#" + this.fieldvalues['ident1']);
        /* clear the div out */
        div1.empty();
        if (val1 !== "") {
            /* string is not empty, so fill in a value */
            div1.html("<input name=\"" +  this.formname('hidden_field1') + "\" value=\"" + val1 +"\" type=\"hidden\" />");
            }
        }

    var val2 = this.fieldarg_in_result('hidden_field2', result, fieldlist);
    if (val2 !== undefined) {
        /* find the div containing the field */
        var div1 = $("#" + this.fieldvalues['ident2']);
        /* clear the div out */
        div2.empty();
        if (val2 !== "") {
            /* string is not empty, so fill in a value */
            div2.html("<input name=\"" +  this.formname('hidden_field2') + "\" value=\"" + val2 +"\" type=\"hidden\" />");
            }
        }

    var val3 = this.fieldarg_in_result('hidden_field3', result, fieldlist);
    if (val3 !== undefined) {
        /* find the div containing the field */
        var div3 = $("#" + this.fieldvalues['ident3']);
        /* clear the div out */
        div3.empty();
        if (val3 !== "") {
            /* string is not empty, so fill in a value */
            div3.html("<input name=\"" +  this.formname('hidden_field3') + "\" value=\"" + val3 +"\" type=\"hidden\" />");
            }
        }

    var val4 = this.fieldarg_in_result('hidden_field4', result, fieldlist);
    if (val4 !== undefined) {
        /* find the div containing the field */
        var div4 = $("#" + this.fieldvalues['ident4']);
        /* clear the div out */
        div4.empty();
        if (val4 !== "") {
            /* string is not empty, so fill in a value */
            div4.html("<input name=\"" +  this.formname('hidden_field4') + "\" value=\"" + val4 +"\" type=\"hidden\" />");
            }
        }

    /* check if an error message or clear_error is given */
    if (this.check_error(fieldlist, result)) {
        return;
        }

    var set_hide = this.fieldarg_in_result('hide', result, fieldlist);
    if (set_hide !== undefined) {
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


SKIPOLE.upload.UploadFile1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.upload.UploadFile1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.upload.UploadFile1.prototype.constructor = SKIPOLE.upload.UploadFile1;

