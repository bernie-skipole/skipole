/*
####### SKIPOLE WEB FRAMEWORK #######

 svggraphs-0.1.0.js  - javascript widgets

 This file is part of the Skipole web framework

 Date : 20180116

 Author : Bernard Czenkusz
 Email  : bernie@skipole.co.uk


   Copyright 2018 Bernard Czenkusz

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


SKIPOLE.svggraphs = {};

SKIPOLE.svggraphs.Chart1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.Chart1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.Chart1.prototype.constructor = SKIPOLE.svggraphs.Chart1;
SKIPOLE.svggraphs.Chart1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);

    var the_widg = this.widg;
    // set the chart values

    var values = this.fieldarg_in_result('values', result, fieldlist);
    if (values == undefined) {
        return;
        }

    var number_of_points = values.length;

    if (!number_of_points) {
        return;
        }

    // calculate points from these values

    var xpoint = 515;
    var points = "";

    values.reverse();

    for (pt = 0; pt < number_of_points; pt++) {
        var ypoint = values[pt];
        xpoint = xpoint-10;
        if (xpoint < 5) {
            break;
            }
        points = points + " " + xpoint + ",";
        if (ypoint > 100){
            points = points + "5";
            }
        else if (ypoint < -100) {
            points = points + "205";
            }
        else {
            points = points + (105-ypoint);
            }
        }

    var line = the_widg.find('polyline');
    if (line == undefined) {
        return;
        }
    line.attr('points', points);
    };

