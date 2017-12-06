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


SKIPOLE.svgbasics.SVGContainer = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.SVGContainer.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.SVGContainer.prototype.constructor = SKIPOLE.svgbasics.SVGContainer;
SKIPOLE.svgbasics.SVGContainer.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('width', 'width', result, fieldlist);
    this.set_attribute('height', 'height', result, fieldlist);
    this.set_attribute('viewBox', 'viewBox', result, fieldlist);
    this.set_attribute('preserveAspectRatio', 'preserveAspectRatio', result, fieldlist);
    };


SKIPOLE.svgbasics.Group = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Group.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Group.prototype.constructor = SKIPOLE.svgbasics.Group;
SKIPOLE.svgbasics.Group.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };


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


SKIPOLE.svgbasics.Circle = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Circle.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Circle.prototype.constructor = SKIPOLE.svgbasics.Circle;
SKIPOLE.svgbasics.Circle.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('cx', 'cx', result, fieldlist);
    this.set_attribute('cy', 'cy', result, fieldlist);
    this.set_attribute('r', 'r', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };


SKIPOLE.svgbasics.Line = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Line.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Line.prototype.constructor = SKIPOLE.svgbasics.Line;
SKIPOLE.svgbasics.Line.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('x1', 'x1', result, fieldlist);
    this.set_attribute('y1', 'y1', result, fieldlist);
    this.set_attribute('x2', 'x2', result, fieldlist);
    this.set_attribute('y2', 'y2', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };


SKIPOLE.svgbasics.Ellipse = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Ellipse.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Ellipse.prototype.constructor = SKIPOLE.svgbasics.Ellipse;
SKIPOLE.svgbasics.Ellipse.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('cx', 'cx', result, fieldlist);
    this.set_attribute('cy', 'cy', result, fieldlist);
    this.set_attribute('rx', 'rx', result, fieldlist);
    this.set_attribute('ry', 'ry', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };


SKIPOLE.svgbasics.Polygon = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Polygon.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Polygon.prototype.constructor = SKIPOLE.svgbasics.Polygon;
SKIPOLE.svgbasics.Polygon.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    var points_table = this.fieldarg_in_result('points', result, fieldlist);
    if (!points_table) {
        return;
        }
    var points = "";
    for(var i = 0, size = points_table.length; i < size ; i++){
        var point = points_table[i];
        points = points.concat(point[0], ",", point[1], " ");
        }
    this.widg.attr("points", points);
    };


SKIPOLE.svgbasics.Polyline = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Polyline.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Polyline.prototype.constructor = SKIPOLE.svgbasics.Polyline;
SKIPOLE.svgbasics.Polyline.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    var points_table = this.fieldarg_in_result('points', result, fieldlist);
    if (!points_table) {
        return;
        }
    var points = "";
    for(var i = 0, size = points_table.length; i < size ; i++){
        var point = points_table[i];
        points = points.concat(point[0], ",", point[1], " ");
        }
    this.widg.attr("points", points);
    };



SKIPOLE.svgbasics.Path = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.Path.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.Path.prototype.constructor = SKIPOLE.svgbasics.Path;
SKIPOLE.svgbasics.Path.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('d', 'd', result, fieldlist);
    this.set_attribute('fill', 'fill', result, fieldlist);
    this.set_attribute('stroke', 'stroke', result, fieldlist);
    this.set_attribute('stroke-width', 'stroke_width', result, fieldlist);
    };



