

SKIPOLE.lists = {};

SKIPOLE.lists.UList1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.lists.UList1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.lists.UList1.prototype.constructor = SKIPOLE.lists.UList1;
SKIPOLE.lists.UList1.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    let fieldvalues = this.fieldvalues;
    // contents
    let contents = this.fieldarg_in_result('contents', result, fieldlist);
    // the class of the elements
    let even_class = fieldvalues["even_class"];
    let odd_class = fieldvalues["odd_class"];

    if (contents) {
        // If a request to renew the list is recieved, this block
        // empties the existing list, and re-draws it
        let rows = contents.length;
        // empty the list
        the_widg.empty();
        // and now start filling it again
        let htmlcontent = "";
        for (row = 0; row < rows; row++) {
            // for each row
            if (even_class && (row % 2)) {
                htmlcontent += "<li class = \"" + even_class + "\">";
                }
            else if (odd_class && (!(row % 2))) {
                htmlcontent += "<li class = \"" + odd_class + "\">";
                }
            else {
                htmlcontent += "<li>";
                }
            htmlcontent += SKIPOLE.textbr(contents[row]);
            // close the cell
            htmlcontent += "</li>";
            }
        the_widg.html(htmlcontent);
        }
    };



SKIPOLE.lists.UList2 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.lists.UList2.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.lists.UList2.prototype.constructor = SKIPOLE.lists.UList2;
SKIPOLE.lists.UList2.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    let fieldvalues = this.fieldvalues;
    // contents
    let contents = this.fieldarg_in_result('set_html', result, fieldlist);
    // the class of the elements
    let even_class = fieldvalues["even_class"];
    let odd_class = fieldvalues["odd_class"];

    if (contents) {
        // If a request to renew the list is recieved, this block
        // empties the existing list, and re-draws it
        let rows = contents.length;
        // empty the list
        the_widg.empty();
        // and now start filling it again
        let htmlcontent = "";
        for (row = 0; row < rows; row++) {
            // for each row
            if (even_class && (row % 2)) {
                htmlcontent += "<li class = \"" + even_class + "\">";
                }
            else if (odd_class && (!(row % 2))) {
                htmlcontent += "<li class = \"" + odd_class + "\">";
                }
            else {
                htmlcontent += "<li>";
                }
            htmlcontent += contents[row];
            // close the cell
            htmlcontent += "</li>";
            }
        the_widg.html(htmlcontent);
        }
    };


SKIPOLE.lists.TableList = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.lists.TableList.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.lists.TableList.prototype.constructor = SKIPOLE.lists.TableList;
SKIPOLE.lists.TableList.prototype.setvalues = function (fieldlist, result) {
   if (!this.widg_id) {
        return;
        }
    let widg_id = this.widg_id
    let the_widg = this.widg;
    let fieldvalues = this.fieldvalues;
    // hide the widget
    let set_hide = this.fieldarg_in_result('hide', result, fieldlist);
    if (set_hide != undefined) {
        if (set_hide) {
            if (the_widg.is(":visible")) {
                the_widg.fadeOut('slow');
                }
            }
        else {
            if (!(the_widg.is(":visible"))) {
                the_widg.fadeIn('slow');
                 }
            }
        }

    // If a request to renew the table is recieved
    // empty the existing table, and re-draw it

    // The table contents
    let contents = this.fieldarg_in_result('contents', result, fieldlist);
    if (contents == undefined){
       return;
       }

    // the class of the button's if any
    let button_class = fieldvalues["button_class"];
    let remove_button_text = fieldvalues["remove_button_text"];
    if (!remove_button_text) {
          remove_button_text = "Remove"
          }

    // the class of the rows
    let even_class = fieldvalues["even_class"];
    let odd_class = fieldvalues["odd_class"];

    // button urls
    let up_link_url = fieldvalues["up_link_url"];
    let down_link_url = fieldvalues["down_link_url"];
    let remove_link_url = fieldvalues["remove_link_url"];

    let maximize_text_col = fieldvalues["maximize_text_col"];

    // empty the table
    the_widg.empty();

    // The table contents
    if (contents) {
        let rows = contents.length;
        // Start filling the empty table
        let htmlcontent = "";
        for (row = 0; row < rows; row++) {
            // for each row in the table
            // row class
            if (even_class && (row % 2)) {
                htmlcontent += "<tr class = \"" + even_class + "\">";
                }
            else if (odd_class && (!(row % 2))) {
                htmlcontent += "<tr class = \"" + odd_class + "\">";
                }
            else {
                htmlcontent += "<tr>";
                }

            // for each row, build the td's from content
      
            let tablerow = contents[row];
            // tablerow is [textitem, upget, downget, removeget]

            // first column is text
            if (maximize_text_col) {
                htmlcontent += "<td style=\"width : 100%;\">";
                }
            else {
                htmlcontent += "<td>";
                }
            htmlcontent += SKIPOLE.textbr(tablerow[0]) + "</td>";

            // 2nd column is uparrow
           if (!row) {
               // row zero has no up button
               htmlcontent += "<td>&nbsp;</td>";
               }
           else if (!up_link_url) {
               htmlcontent += "<td>Warning: broken link</td>";
               }
           else {
                // its a link, apply button class
                htmlcontent += "<td>"
                let url = up_link_url;
                if (button_class) {
                    htmlcontent +=  "<a role=\"button\" class=\"" + button_class + "\"";
                    }
                else {
                    htmlcontent +=  "<a role=\"button\"";
                    }
                // get url and create href attribute
                if (tablerow[1]) {
                    url += "?ident=" + SKIPOLE.identdata + "&" + this.formname("contents") + "=" + tablerow[1];
                    }
                else {
                    url += "?ident=" + SKIPOLE.identdata;
                    }
                htmlcontent +=  " href=\"" + url + "\">&uarr;</a></td>";
                }


            // 3rd column is downarrow
           if (row == rows-1) {
               // last row has no down button
               htmlcontent += "<td>&nbsp;</td>";
               }
           else if (!down_link_url) {
               htmlcontent += "<td>Warning: broken link</td>";
               }
           else {
                // its a link, apply button class
                htmlcontent += "<td>"
                let url = down_link_url;
                if (button_class) {
                    htmlcontent +=  "<a role=\"button\" class=\"" + button_class + "\"";
                    }
                else {
                    htmlcontent +=  "<a role=\"button\"";
                    }
                // get url and create href attribute
                if (tablerow[2]) {
                    url += "?ident=" + SKIPOLE.identdata + "&" + this.formname("contents") + "=" + tablerow[2];
                    }
                else {
                    url += "?ident=" + SKIPOLE.identdata;
                    }
                htmlcontent +=  " href=\"" + url + "\">&darr;</a></td>";
                }

            // 4th column is Remove
           if (!remove_link_url) {
               htmlcontent += "<td>Warning: broken link</td>";
               }
           else {
                // its a link, apply button class
                htmlcontent += "<td>"
                let url = remove_link_url;
                if (button_class) {
                    htmlcontent +=  "<a role=\"button\" class=\"" + button_class + "\"";
                    }
                else {
                    htmlcontent +=  "<a role=\"button\"";
                    }
                // get url and create href attribute
                if (tablerow[3]) {
                    url += "?ident=" + SKIPOLE.identdata + "&" + this.formname("contents") + "=" + tablerow[3];
                    }
                else {
                    url += "?ident=" + SKIPOLE.identdata;
                    }
                htmlcontent +=  " href=\"" + url + "\">" + remove_button_text + "</a></td>";
                }

            // close the row
            htmlcontent += "</tr>";
            }
        the_widg.html(htmlcontent);
        // as table was emptied, a new click event has to be applied to the buttons
        $("#" + widg_id + " a").click(function (e) {
              SKIPOLE.widgets[widg_id].eventfunc(e);
              });
        }

    };

SKIPOLE.lists.TableList.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    if (!this.widg_id) {
        return;
        }
    let fieldvalues = this.fieldvalues;
    let button = $(e.target);
    let href = button.attr('href');
    if (!href) {
        return;
        }

    let senddata = href.substring(href.indexOf('?')+1);

    /* col 0 is text, no link
       col 1 calls up_json_url,
       col 2 calls down_json_url,
       col 3 calls remove_json_url

       So need to find the column of the target to find which json url to call */

    let col = button.parent().index();
    let json_url = "";

    if (col == 1) {
                   json_url = fieldvalues["up_json_url"];
                  }
    else if (col == 2) {
                   json_url = fieldvalues["down_json_url"];
                  }
    else if (col == 3) {
                   json_url = fieldvalues["remove_json_url"];
                       }
    else {
          return;
         }

    if (!json_url) {
          return;
          }

    // so we have a json_url to call, and senddata has the query string

    e.preventDefault();
    // respond to json or html
    $.ajax({
          url: json_url,
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




