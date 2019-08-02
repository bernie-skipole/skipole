
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

    var pointcol = this.fieldvalues['pointcol'];
    var mx = this.fieldvalues['mx'];
    var my = this.fieldvalues['my'];
    var cx = this.fieldvalues['cx'];
    var cy = this.fieldvalues['cy'];
    var minx = this.fieldvalues['minx'];
    var maxx = this.fieldvalues['maxx'];
    var miny = this.fieldvalues['miny'];
    var maxy = this.fieldvalues['maxy'];

    var graphstring = "";

    // delete existing points
    the_widg.empty();
    // draw new points
    for (pt = 0; pt < number_of_points; pt++) {
        var xpoint = parseFloat(values[pt][0]);
        var ypoint = parseFloat(values[pt][1]);
        var x = Math.floor(mx*xpoint + cx);
        var y = Math.floor(my*ypoint + cy);
        if (ypoint<miny) {continue;}
        if (ypoint>maxy) {continue;}
        if (xpoint<minx) {continue;}
        if (xpoint>maxx) {continue;}
        graphstring += "<line x1=\"" + x +"\" y1=\"" + (y-5) + "\" x2=\"" + x + "\" y2=\"" + (y+5) + "\" stroke=\"" + pointcol + "\" stroke-width=\"1\" />";
        graphstring += "<line x1=\"" + (x-5) +"\" y1=\"" + y + "\" x2=\"" + (x+5) + "\" y2=\"" + y + "\" stroke=\"" + pointcol + "\" stroke-width=\"1\" />";
        }
    the_widg.html(graphstring);
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

    var linecol = this.fieldvalues['linecol'];
    var linewidth = this.fieldvalues['linewidth'];
    var pointradius = this.fieldvalues['pointradius'];
    var mx = this.fieldvalues['mx'];
    var my = this.fieldvalues['my'];
    var cx = this.fieldvalues['cx'];
    var cy = this.fieldvalues['cy'];
    var minx = this.fieldvalues['minx'];
    var maxx = this.fieldvalues['maxx'];
    var miny = this.fieldvalues['miny'];
    var maxy = this.fieldvalues['maxy'];

    var graphstring = "";

    // delete existing points
    the_widg.empty();
    // draw new points

    var old_x = '';
    var old_y = '';

    for (pt = 0; pt < number_of_points; pt++) {
        var xpoint = parseFloat(values[pt][0]);
        var ypoint = parseFloat(values[pt][1]);
        var x = Math.floor(mx*xpoint + cx);
        var y = Math.floor(my*ypoint + cy);
        if (ypoint<miny) {continue;}
        if (ypoint>maxy) {continue;}
        if (xpoint<minx) {continue;}
        if (xpoint>maxx) {continue;}
        graphstring += "<circle cx=\"" + x +"\" cy=\"" + y + "\" r=\"" + pointradius + "\" fill=\"" + linecol + "\" stroke=\"" + linecol + "\" />";
        if (old_x && linewidth) {
            graphstring += "<line x1=\"" + old_x +"\" y1=\"" + old_y + "\" x2=\"" + x + "\" y2=\"" + y + "\" stroke=\"" + linecol + "\" stroke-width=\"" + linewidth + "\" />";
            }
        old_x = x;
        old_y = y;
        }
    the_widg.html(graphstring);
    };


