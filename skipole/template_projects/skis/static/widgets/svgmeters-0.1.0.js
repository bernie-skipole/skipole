
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


SKIPOLE.svgmeters.Traditional1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgmeters.Traditional1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgmeters.Traditional1.prototype.constructor = SKIPOLE.svgmeters.Traditional1;
SKIPOLE.svgmeters.Traditional1.prototype.setvalues = function (fieldlist, result) {
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
    var circle = the_widg.find('circle');
    if (circle == undefined) {
        return;
        }
    var arrow_stroke = this.fieldarg_in_result('arrow_stroke', result, fieldlist);
    if (arrow_stroke) {
        arrow.attr('stroke', arrow_stroke);
        circle.attr('stroke', arrow_stroke);
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
        arrow.attr('transform', "rotate(60 350 350)");
        return;
        }
    if (m <= mn) {
        arrow.attr('transform', "rotate(-60 350 350)");
        return;
        }

    var scale = Math.round((m-mn)*120/(mx-mn) - 60);
    arrow.attr('transform', "rotate(" + scale + " 350 350)");
    };



