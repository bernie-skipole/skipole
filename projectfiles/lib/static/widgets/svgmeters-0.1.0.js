/*
####### SKIPOLE WEB FRAMEWORK #######

 svgmeters-0.1.0.js  - javascript widgets

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


SKIPOLE.svgmeters = {};


SKIPOLE.svgmeters.Arrow1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgmeters.Arrow1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgmeters.Arrow1.prototype.constructor = SKIPOLE.svgmeters.Arrow1;
SKIPOLE.svgmeters.Arrow1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };


SKIPOLE.svgmeters.Arrow2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgmeters.Arrow2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgmeters.Arrow2.prototype.constructor = SKIPOLE.svgmeters.Arrow2;
SKIPOLE.svgmeters.Arrow2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };


SKIPOLE.svgmeters.Vertical1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgmeters.Vertical1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgmeters.Vertical1.prototype.constructor = SKIPOLE.svgmeters.Vertical1;
SKIPOLE.svgmeters.Vertical1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    var the_widg = this.widg;
    // set the fill attribute of the polygon
    var arrow = the_widg.find('polygon');
    if (arrow == undefined) {
        return;
        }
    var arrow_fill = this.fieldarg_in_result('arrow_fill', result, fieldlist);
    if (arrow_fill) {
        arrow.attr('fill', arrow_fill);
        }

    // set the measurement
    var measurement = this.fieldarg_in_result('measurement', result, fieldlist);
    if (measurement == undefined) {
        return;
        }

    var minvalue = this.fieldvalues["minvalue"];
    var maxvalue = this.fieldvalues["maxvalue"];
    if (minvalue == undefined) {
        return;
        }
    if (maxvalue == undefined) {
        return;
        }

    var m = parseFloat(measurement);
    var mn = parseFloat(minvalue);
    var mx = parseFloat(maxvalue);

    if (m >= mx) {
        arrow.attr('transform', "translate(0, 0)");
        return;
        }
    if (m <= mn) {
        arrow.attr('transform', "translate(0, 600)");
        return;
        }

    var scale = Math.round(600 - (m - mn)*600/(mx-mn));
    arrow.attr('transform', "translate(0, " + scale + ")");
    };






