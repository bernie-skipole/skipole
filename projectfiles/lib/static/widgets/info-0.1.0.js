/*
####### SKIPOLE WEB FRAMEWORK #######

 info-0.1.0.js  - javascript widgets

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


SKIPOLE.info = {};

SKIPOLE.info.ServerTimeStamp = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.info.ServerTimeStamp.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.info.ServerTimeStamp.prototype.constructor = SKIPOLE.info.ServerTimeStamp;
SKIPOLE.info.ServerTimeStamp.prototype.show_error = function (error_message) {
    if (!error_message) {
        error_message = this.error_message;
        }
    if (!error_message) {
        error_message = "Unknown Error";
        }
    var the_widg = this.widg;
    the_widg.attr("data-status", "error");
    the_widg.text(error_message);
    if ("error_class" in this.fieldvalues) {
         the_widg.attr("class", this.fieldvalues["error_class"]);
        }
    };
SKIPOLE.info.ServerTimeStamp.prototype.clear_error = function () {
    /* prototype clears data-status  */
    var the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    };
SKIPOLE.info.ServerTimeStamp.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    /* check if an error message or clear_error is given */
    this.check_error(fieldlist, result);
    // timestamp
    var timestamp_text = this.fieldarg_in_result('timestamp', result, fieldlist);
    if (timestamp_text) {
        this.widg.text(timestamp_text);
        }
    };


SKIPOLE.info.PageIdent = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.info.PageIdent.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.info.PageIdent.prototype.constructor = SKIPOLE.info.PageIdent;
SKIPOLE.info.PageIdent.prototype.show_error = function (error_message) {
    if (!error_message) {
        error_message = this.error_message;
        }
    if (!error_message) {
        error_message = "Unknown Error";
        }
    var the_widg = this.widg;
    the_widg.attr("data-status", "error");
    the_widg.text(error_message);
    if ("error_class" in this.fieldvalues) {
         the_widg.attr("class", this.fieldvalues["error_class"]);
        }
    };
SKIPOLE.info.PageIdent.prototype.clear_error = function () {
    /* prototype clears data-status  */
    var the_widg = this.widg;
    if (the_widg.attr("data-status") == "error") {
        the_widg.removeAttr( "data-status" )
        }
    };


SKIPOLE.info.Redirector = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.info.Redirector.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.info.Redirector.prototype.constructor = SKIPOLE.info.Redirector;


SKIPOLE.info.Version = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.info.Version.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.info.Version.prototype.constructor = SKIPOLE.info.Version;


SKIPOLE.info.SkipoleVersion = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.info.SkipoleVersion.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.info.SkipoleVersion.prototype.constructor = SKIPOLE.info.SkipoleVersion;





