
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

    var xpoint = 510;
    var points = "";

    values.reverse();

    for (pt = 0; pt < number_of_points; pt++) {
        var ypoint = values[pt];
        xpoint = xpoint-10;
        if (xpoint < 0) {
            break;
            }
        points = points + " " + xpoint + ",";
        if (ypoint > 100){
            points = str(points);
            }
        else if (ypoint < -100) {
            points = points + "200";
            }
        else {
            points = points + (100-ypoint);
            }
        }

    var line = the_widg.find('polyline');
    if (line == undefined) {
        return;
        }
    line.attr('points', points);
    };


SKIPOLE.svggraphs.StarChart = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.StarChart.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.StarChart.prototype.constructor = SKIPOLE.svggraphs.StarChart;
SKIPOLE.svggraphs.StarChart.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };


SKIPOLE.svggraphs.Graph48Hr = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.Graph48Hr.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.Graph48Hr.prototype.constructor = SKIPOLE.svggraphs.Graph48Hr;
SKIPOLE.svggraphs.Graph48Hr.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };


SKIPOLE.svggraphs.Axis1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.Axis1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.Axis1.prototype.constructor = SKIPOLE.svggraphs.Axis1;
SKIPOLE.svggraphs.Axis1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };

SKIPOLE.svggraphs.Axis2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.Axis2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.Axis2.prototype.constructor = SKIPOLE.svggraphs.Axis2;
SKIPOLE.svggraphs.Axis2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };


SKIPOLE.svggraphs.Points = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.Points.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.Points.prototype.constructor = SKIPOLE.svggraphs.Points;
SKIPOLE.svggraphs.Points.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };


SKIPOLE.svggraphs.Lines = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svggraphs.Lines.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svggraphs.Lines.prototype.constructor = SKIPOLE.svggraphs.Lines;
SKIPOLE.svggraphs.Lines.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    this.set_attribute('transform', 'transform', result, fieldlist);
    };

