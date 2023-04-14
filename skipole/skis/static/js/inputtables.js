

SKIPOLE.inputtables = {};


SKIPOLE.inputtables.InputTable1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputtables.InputTable1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputtables.InputTable1.prototype.constructor = SKIPOLE.inputtables.InputTable1;
SKIPOLE.inputtables.InputTable1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    // columns
    let col1 = this.fieldarg_in_result('col1', result, fieldlist);
    let col2 = this.fieldarg_in_result('col2', result, fieldlist);
    let row_classes = this.fieldarg_in_result('row_classes', result, fieldlist);
    let keysvals = this.fieldarg_in_result('inputdict', result, fieldlist);
    let cell_style = this.fieldarg_in_result('cell_style', result, fieldlist);
    let self = this;

    let tbody = the_widg.find('tbody');
    if (!tbody.length) {
        return;
        }

    let index = 0;
    tbody.find('tr').each(function() {
        // for each row in the body

        // set its class
        if (row_classes && row_classes.length) {
            if (row_classes[index] !== null) {
                $(this).attr("class", row_classes[index]);
                }
            }
        // for the td cells in the row
        let cells = $(this).children();
        if (col1 && col1.length) {
            if (col1[index] !== null) {
                $(cells[0]).text(col1[index]);
                }
             }
        if (col2 && col2.length) {
            if (col2[index] !== null) {
                $(cells[1]).text(col2[index]);
                }
             }

         //deal with input field
        let inputtag = $(cells[2]).find('input');

        if (keysvals != undefined) {
            // If inputdict given, any value for this
            // row should be set
            let inputname = inputtag.prop('name');
            // get the rowkey from this name, which should be of the form
            // widgetname:fieldname-rowkey
            let namearray = inputname.split("-");
            let rowkey = namearray[1];
            if (rowkey in keysvals) {
                if (keysvals[rowkey] !== null) {
                    // the received inputdict has a new value for this row
                    inputtag.val(keysvals[rowkey]);
                    }
                }
             }
         index=index+1;
        })

    // set cell colours
    if (cell_style != undefined) {
        bodyrows = tbody.find('tr');

        cell_style.forEach(function (item, index) {
            // for each inner list of cell_style which is of format [row, col, style]
            let row = bodyrows[item[0]-1];
            let columns = $(row).find('td');
            let cell = columns[item[1]-1];
            if (item[2]) {
                $(cell).attr('style', item[2]);
                }
            else {
                $(cell).removeAttr('style');
                }
            });
        }

    };



SKIPOLE.inputtables.InputTable5 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputtables.InputTable5.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputtables.InputTable5.prototype.constructor = SKIPOLE.inputtables.InputTable5;
SKIPOLE.inputtables.InputTable5.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    // input_accepted and input_errored
    let input_accepted = this.fieldarg_in_result('set_input_accepted', result, fieldlist);
    let input_errored = this.fieldarg_in_result('set_input_errored', result, fieldlist);
    let self = this;
    let inputindex = 0;
    the_widg.find('input[type="text"]').each(function() {
        // for each text input field, get its index key
        let text_input = $(this);
        if (text_input.prop('disabled')) {
            return true;
            }
        // get the index key of this input field
        let input_key = inputindex.toString();
        inputindex += 1;
        if (input_accepted) {
            if (input_key in input_accepted) {
                self.set_accepted(text_input, input_accepted[input_key]);
                }
            }
        if (input_errored) {
            if (input_key in input_errored) {
                self.set_errored(text_input, input_errored[input_key]);
                }
            }
        })
    };

SKIPOLE.inputtables.InputTable5.prototype.setbutton = function(name, value) {
    // Called by button onclick, to save the name,value of the button
    // used to submit the form
    this.button_name = name;
    this.button_value = value;
    };

SKIPOLE.inputtables.InputTable5.prototype.eventfunc = function(e) {
    SKIPOLE.skiprefresh = true;
    let selected_form = $(e.target);
    if (!SKIPOLE.form_validate(selected_form)) {
        // prevent the submission if validation failure
        e.preventDefault();
        }
    else {
        // form validated, if action_json url set, call a json page
        let jsonurl = this.fieldvalues["url"];
        if (jsonurl) {
            // json url set, send data with a request for json and prevent default
            let self = this
            let senddata = selected_form.serializeArray();
            // get the submit button name, value which submitted this form
            // this is necessary since serializeArray() does not pick up the button name
            // and value from the form, so an onclick event saves them using setbutton()
            // and the name,value is pushed on to senddata
            senddata.push({ name:this.button_name, value:this.button_value });
            e.preventDefault();
            // respond to json or html
            $.ajax({
                  url: jsonurl,
                  data: senddata
                      })
                  .done(function(result, textStatus, jqXHR) {
                     if (jqXHR.responseJSON) {
                          // JSON response
                          if (self.get_error(result)) {
                              // if error, set any results received from the json call
                              SKIPOLE.setfields(result);
                              }
                          else {
                              // If no error received, clear any previous error
                              self.clear_error();
                              SKIPOLE.setfields(result);
                              }
                           } else {
                              // html response
                              document.open();
                              document.write(result);
                              document.close();
                              }
                      })
                  .fail(function( jqXHR, textStatus, errorThrown ) {
                              if (jqXHR.status == 400 || jqXHR.status == 404 || jqXHR.status == 500)  {
                                  document.open();
                                  document.write(jqXHR.responseText);
                                  document.close();
                                  }
                              else {
                                  SKIPOLE.json_failed( jqXHR, textStatus, errorThrown );
                                  }
                      });
            }
        }
    };



SKIPOLE.inputtables.InputTable4 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputtables.InputTable4.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputtables.InputTable4.prototype.constructor = SKIPOLE.inputtables.InputTable4;
SKIPOLE.inputtables.InputTable4.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    // columns
    let col1 = this.fieldarg_in_result('col1', result, fieldlist);
    let col2 = this.fieldarg_in_result('col2', result, fieldlist);
    let col3 = this.fieldarg_in_result('col3', result, fieldlist);
    let row_classes = this.fieldarg_in_result('row_classes', result, fieldlist);
    let up_hide = this.fieldarg_in_result('up_hide', result, fieldlist);
    let down_hide = this.fieldarg_in_result('down_hide', result, fieldlist);
    let keysvals = this.fieldarg_in_result('inputdict', result, fieldlist);
    let cell_style = this.fieldarg_in_result('cell_style', result, fieldlist);
    let self = this;

    let tbody = the_widg.find('tbody');
    if (!tbody.length) {
        return;
        }

    let index = 0;
    tbody.find('tr').each(function() {
            // for each row in the body

            // set its class
            if (row_classes && row_classes.length) {
                if (row_classes[index] !== null) {
                    $(this).attr("class", row_classes[index]);
                    }
                }
            let cells = $(this).children();
            if (col1 && col1.length) {
                if (col1[index] !== null) {
                    $(cells[0]).text(col1[index]);
                    }
                 }
            if (col2 && col2.length) {
                if (col2[index] !== null) {
                    $(cells[1]).text(col2[index]);
                    }
                 }
            if (col3 && col3.length) {
                if (col3[index] !== null) {
                    $(cells[2]).text(col3[index]);
                    }
                 }

            let a_link = $(cells[3]).find("a");
            let up_link = $(a_link[0]);
            // up_getfield1
            let up_getfield1 = self.fieldarg_in_result('up_getfield1', result, fieldlist);
            if (up_getfield1 && up_getfield1.length) {
                if (up_getfield1[index] !== null) {
                    let href = up_link.attr('href');
                    let url = self.setgetfield(href, 'up_getfield1',up_getfield1[index]);
                    up_link.attr('href', url);
                    }
                }
            // up_getfield2
            let up_getfield2 = self.fieldarg_in_result('up_getfield2', result, fieldlist);
            if (up_getfield2 && up_getfield2.length) {
                if (up_getfield2[index] !== null) {
                    let href = up_link.attr('href');
                    let url = self.setgetfield(href, 'up_getfield2', up_getfield2[index]);
                    up_link.attr('href', url);
                    }
                }
            // up_hide
            if (up_hide && up_hide.length) {
                if (up_hide[index] !== null) {
                    if (up_hide[index] === true) {
                        up_link.css("visibility", "hidden");
                        }
                    else {
                        up_link.css("visibility", "visible");
                        }
                    }
                }

            let down_link = $(a_link[1]);
            // down_getfield1
            let down_getfield1 = self.fieldarg_in_result('down_getfield1', result, fieldlist);
            if (down_getfield1 && down_getfield1.length) {
                if (down_getfield1[index] !== null) {
                    let href = down_link.attr('href');
                    let url = self.setgetfield(href, 'down_getfield1',down_getfield1[index]);
                    down_link.attr('href', url);
                    }
                }
            // down_getfield2
            let down_getfield2 = self.fieldarg_in_result('down_getfield2', result, fieldlist);
            if (down_getfield2 && down_getfield2.length) {
                if (down_getfield2[index] !== null) {
                    let href = down_link.attr('href');
                    let url = self.setgetfield(href, 'down_getfield2', down_getfield2[index]);
                    down_link.attr('href', url);
                    }
                }
            // down_hide
            if (down_hide && down_hide.length) {
                if (down_hide[index] !== null) {
                    if (down_hide[index] === true) {
                        down_link.css("visibility", "hidden");
                        }
                    else {
                        down_link.css("visibility", "visible");
                        }
                    }
                }

            //deal with input field
            let inputtag = $(cells[3]).find('input');

            if (keysvals != undefined) {
                // If inputdict given, any value for this
                // row should be set
                let inputname = inputtag.prop('name');
                // get the rowkey from this name, which should be of the form
                // widgetname:fieldname-rowkey
                let namearray = inputname.split("-");
                let rowkey = namearray[1];
                if (rowkey in keysvals) {
                    if (keysvals[rowkey] !== null) {
                        // the received inputdict has a new value for this row
                        inputtag.val(keysvals[rowkey]);
                        }
                    }
                 }

             index=index+1;
        })

    // set cell colours
    if (cell_style != undefined) {
        bodyrows = tbody.find('tr');

        cell_style.forEach(function (item, index) {
            // for each inner list of cell_style which is of format [row, col, style]
            let row = bodyrows[item[0]-1];
            let columns = $(row).find('td');
            let cell = columns[item[1]-1];
            if (item[2]) {
                $(cell).attr('style', item[2]);
                }
            else {
                $(cell).removeAttr('style');
                }
            });
        }
    };
SKIPOLE.inputtables.InputTable4.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    if (!this.widg_id) {
        return;
        }
    let fieldvalues = this.fieldvalues;
    let the_widg = this.widg;
    let button_pressed = $(e.target);

    if (button_pressed.text() == "\u2191") {
        // up arrow button
        if (!fieldvalues["upurl"]) {
            // no json url, return and call html link
            return;
            }
        var url = fieldvalues["upurl"];
      }
    else if (button_pressed.text() == "\u2193") {
        // down arrow button
        if (!fieldvalues["downurl"]) {
            // no json url, return and call html link
            return;
            }
        var url = fieldvalues["downurl"];
      }
    else {
      // not known
      return;
      }

    let href = button_pressed.attr('href');
    let senddata = href.substring(href.indexOf('?')+1);
    e.preventDefault();
    // respond to json or html
    $.ajax({
          url: url,
          data: senddata
              })
          .done(function(result, textStatus, jqXHR) {
             if (jqXHR.responseJSON) {
                  // JSON response
                  SKIPOLE.setfields(result);
                  } else {
                      // html response
                      document.open();
                      document.write(result);
                      document.close();
                      }
              })
          .fail(function( jqXHR, textStatus, errorThrown ) {
                      if (jqXHR.status == 400 || jqXHR.status == 404 || jqXHR.status == 500)  {
                          document.open();
                          document.write(jqXHR.responseText);
                          document.close();
                          }
                      else {
                          SKIPOLE.json_failed( jqXHR, textStatus, errorThrown );
                          }
              });

    };


SKIPOLE.inputtables.InputTable3 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.inputtables.InputTable3.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.inputtables.InputTable3.prototype.constructor = SKIPOLE.inputtables.InputTable3;
SKIPOLE.inputtables.InputTable3.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    // columns
    let col1 = this.fieldarg_in_result('col1', result, fieldlist);
    let col2 = this.fieldarg_in_result('col2', result, fieldlist);

    let up_getfield1 = this.fieldarg_in_result('up_getfield1', result, fieldlist);
    let up_getfield2 = this.fieldarg_in_result('up_getfield2', result, fieldlist);
    let down_getfield1 = this.fieldarg_in_result('down_getfield1', result, fieldlist);
    let down_getfield2 = this.fieldarg_in_result('down_getfield2', result, fieldlist);


    let row_classes = this.fieldarg_in_result('row_classes', result, fieldlist);
    let up_hide = this.fieldarg_in_result('up_hide', result, fieldlist);
    let down_hide = this.fieldarg_in_result('down_hide', result, fieldlist);
    let keysvals = this.fieldarg_in_result('inputdict', result, fieldlist);
    let cell_style = this.fieldarg_in_result('cell_style', result, fieldlist);
    let self = this;

    let tbody = the_widg.find('tbody');
    if (!tbody.length) {
        return;
        }

    let index = 0;
    tbody.find('tr').each(function() {
            // for each row in the body

            // set the row class
            if (row_classes && row_classes.length) {
                if (row_classes[index] !== null) {
                    $(this).attr("class", row_classes[index]);
                    }
                }
            // for the td cells in the row
            let cells = $(this).children();
            // set col1 value if given
            if (col1 && col1.length) {
                if (col1[index] !== null) {
                    $(cells[0]).text(col1[index]);
                    }
                 }
            // set col2 value if given
            if (col2 && col2.length) {
                if (col2[index] !== null) {
                    $(cells[1]).text(col2[index]);
                    }
                 }

             //deal with input field
            let inputtag = $(cells[2]).find('input');

            if (keysvals != undefined) {
                // If inputdict given, any value for this
                // row should be set
                let inputname = inputtag.prop('name');
                // get the rowkey from this name, which should be of the form
                // widgetname:fieldname-rowkey
                let namearray = inputname.split("-");
                let rowkey = namearray[1];
                if (rowkey in keysvals) {
                    if (keysvals[rowkey] !== null) {
                        // the received inputdict has a new value for this row
                        inputtag.val(keysvals[rowkey]);
                        }
                    }
                 }

            // getf3 for the arrows
            getf3 = inputtag.val();


            let a_link = $(cells[3]).find("a");
            let up_link = $(a_link[0]);
            // up_getfield1
            if (up_getfield1 && up_getfield1.length) {
                if (up_getfield1[index] !== null) {
                    let href = up_link.attr('href');
                    let url = self.setgetfield(href, 'up_getfield1',up_getfield1[index]);
                    up_link.attr('href', url);
                    }
                }
            // up_getfield2
            if (up_getfield2 && up_getfield2.length) {
                if (up_getfield2[index] !== null) {
                    let href = up_link.attr('href');
                    let url = self.setgetfield(href, 'up_getfield2', up_getfield2[index]);
                    up_link.attr('href', url);
                    }
                }
            // getfield3
            if (getf3 !== null) {
                let href = up_link.attr('href');
                let url = self.setgetfield(href, 'getfield3', getf3);
                up_link.attr('href', url);
                }
            // up_hide
            if (up_hide && up_hide.length) {
                if (up_hide[index] !== null) {
                    if (up_hide[index] === true) {
                        up_link.css("visibility", "hidden");
                        }
                    else {
                        up_link.css("visibility", "visible");
                        }
                    }
                }

            let down_link = $(a_link[1]);
            // down_getfield1
            if (down_getfield1 && down_getfield1.length) {
                if (down_getfield1[index] !== null) {
                    let href = down_link.attr('href');
                    let url = self.setgetfield(href, 'down_getfield1',down_getfield1[index]);
                    down_link.attr('href', url);
                    }
                }
            // down_getfield2
            if (down_getfield2 && down_getfield2.length) {
                if (down_getfield2[index] !== null) {
                    let href = down_link.attr('href');
                    let url = self.setgetfield(href, 'down_getfield2', down_getfield2[index]);
                    down_link.attr('href', url);
                    }
                }
            // getfield3
            if (getf3 !== null) {
                let href = down_link.attr('href');
                let url = self.setgetfield(href, 'getfield3', getf3);
                down_link.attr('href', url);
                }
            // down_hide
            if (down_hide && down_hide.length) {
                if (down_hide[index] !== null) {
                    if (down_hide[index] === true) {
                        down_link.css("visibility", "hidden");
                        }
                    else {
                        down_link.css("visibility", "visible");
                        }
                    }
                }

             index=index+1;
        })

    // set cell colours
    if (cell_style != undefined) {
        bodyrows = tbody.find('tr');

        cell_style.forEach(function (item, index) {
            // for each inner list of cell_style which is of format [row, col, style]
            let row = bodyrows[item[0]-1];
            let columns = $(row).find('td');
            let cell = columns[item[1]-1];
            if (item[2]) {
                $(cell).attr('style', item[2]);
                }
            else {
                $(cell).removeAttr('style');
                }
            });
        }
    };
SKIPOLE.inputtables.InputTable3.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    if (!this.widg_id) {
        return;
        }
    let fieldvalues = this.fieldvalues;
    let the_widg = this.widg;
    let button_pressed = $(e.target);

    if (button_pressed.text() == "\u2191") {
        // up arrow button
        if (!fieldvalues["upurl"]) {
            // no json url, return and call html link
            return;
            }
        var url = fieldvalues["upurl"];
      }
    else if (button_pressed.text() == "\u2193") {
        // down arrow button
        if (!fieldvalues["downurl"]) {
            // no json url, return and call html link
            return;
            }
        var url = fieldvalues["downurl"];
      }
    else {
      // not known
      return;
      }

    let href = button_pressed.attr('href');
    let senddata = href.substring(href.indexOf('?')+1);
    e.preventDefault();
    // respond to json or html
    $.ajax({
          url: url,
          data: senddata
              })
          .done(function(result, textStatus, jqXHR) {
             if (jqXHR.responseJSON) {
                  // JSON response
                  SKIPOLE.setfields(result);
                  } else {
                      // html response
                      document.open();
                      document.write(result);
                      document.close();
                      }
              })
          .fail(function( jqXHR, textStatus, errorThrown ) {
                      if (jqXHR.status == 400 || jqXHR.status == 404 || jqXHR.status == 500)  {
                          document.open();
                          document.write(jqXHR.responseText);
                          document.close();
                          }
                      else {
                          SKIPOLE.json_failed( jqXHR, textStatus, errorThrown );
                          }
              });

    };

SKIPOLE.inputtables.InputTable3.prototype.setnewnumber = function (val, rownumber) {
    // val is the new value set in the input field, which is now to
    // be put into the getfield3 fields of the arrow links
    // rownumber is the row on the table affected

    let tbody = this.widg.find('tbody');

    let rows = tbody.find('tr');
    let cells = $(rows[rownumber]).children();
    let a_link = $(cells[3]).find("a");

    let up_link = $(a_link[0]);
    let uphref = up_link.attr('href');
    let upurl = this.setgetfield(uphref, 'getfield3', val);
    up_link.attr('href', upurl);

    let down_link = $(a_link[1]);
    let downhref = down_link.attr('href');
    let downurl = this.setgetfield(downhref, 'getfield3', val);
    down_link.attr('href', downurl);
    };
