/*
####### SKIPOLE WEB FRAMEWORK #######

 svgbasics-0.1.0.js  - javascript widgets

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


SKIPOLE.svgbasics = {};


SKIPOLE.svgbasics.Rect = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Rect.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Rect.prototype.constructor = SKIPOLE.svgbasics.Rect;
SKIPOLE.svgbasics.Rect.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    this.set_attribute('x', 'x', result, fieldlist);
    this.set_attribute('y', 'y', result, fieldlist);
    this.set_attribute('rx', 'rx', result, fieldlist);
    this.set_attribute('ry', 'ry', result, fieldlist);
    this.set_attribute('width', 'width', result, fieldlist);
    this.set_attribute('height', 'height', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };



SKIPOLE.svgbasics.SimpleText = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.SimpleText.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.SimpleText.prototype.constructor = SKIPOLE.svgbasics.SimpleText;
SKIPOLE.svgbasics.SimpleText.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    this.set_attribute('x', 'x', result, fieldlist);
    this.set_attribute('y', 'y', result, fieldlist);
    this.set_attribute('dx', 'dx', result, fieldlist);
    this.set_attribute('dy', 'dy', result, fieldlist);
    this.set_attribute('font-family', 'font_family', result, fieldlist);
    this.set_attribute('font-size', 'font_size', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);

    var element_text = this.fieldarg_in_result('text', result, fieldlist);
    if (element_text) {
        this.widg.text(element_text);
        }

    };




