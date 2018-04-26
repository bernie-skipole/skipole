/*
####### SKIPOLE WEB FRAMEWORK #######

 debug_tools-0.1.0.js  - javascript widgets

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


SKIPOLE.debug_tools = {};

SKIPOLE.debug_tools.ShowEnviron = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    if ( SKIPOLE.widget_register.hasOwnProperty("debug_tools.ShowEnviron") ) {
        SKIPOLE.widget_register["debug_tools.ShowEnviron"].push(widg_id);
        }
    else {
        SKIPOLE.widget_register["debug_tools.ShowEnviron"] = [widg_id];
        }
    };
SKIPOLE.debug_tools.ShowEnviron.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.debug_tools.ShowEnviron.prototype.constructor = SKIPOLE.debug_tools.ShowEnviron;
SKIPOLE.debug_tools.ShowEnviron.prototype.updatefunc = function (arg) {
    var thispre = this.widg.find('pre');
    thispre.html(arg);
    };


SKIPOLE.debug_tools.ShowCallData = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    if ( SKIPOLE.widget_register.hasOwnProperty("debug_tools.ShowCallData") ) {
        SKIPOLE.widget_register["debug_tools.ShowCallData"].push(widg_id);
        }
    else {
        SKIPOLE.widget_register["debug_tools.ShowCallData"] = [widg_id];
        }
    };
SKIPOLE.debug_tools.ShowCallData.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.debug_tools.ShowCallData.prototype.constructor = SKIPOLE.debug_tools.ShowCallData;
SKIPOLE.debug_tools.ShowCallData.prototype.updatefunc = function (arg) {
    var thispre = this.widg.find('pre');
    thispre.html(arg);
    };


SKIPOLE.debug_tools.ShowResponders = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    if ( SKIPOLE.widget_register.hasOwnProperty("debug_tools.ShowResponders") ) {
        SKIPOLE.widget_register["debug_tools.ShowResponders"].push(widg_id);
        }
    else {
        SKIPOLE.widget_register["debug_tools.ShowResponders"] = [widg_id];
        }
    };
SKIPOLE.debug_tools.ShowResponders.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.debug_tools.ShowResponders.prototype.constructor = SKIPOLE.debug_tools.ShowResponders;
SKIPOLE.debug_tools.ShowResponders.prototype.updatefunc = function (arg) {
    var thistable = this.widg.find('table');
    // empty the table
    thistable.empty();
    // and now start filling it again
    var rows = arg.length;
    var htmlcontent = "";
    for (row = 0; row < rows; row++) {
        // for each row in the table
        htmlcontent += "<tr><td>" + arg[row][0] + "</td><td>" + arg[row][1] + "</td><td>" + arg[row][2] + "</td></tr>";
        }
    thistable.html(htmlcontent);
    };


