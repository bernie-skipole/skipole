

SKIPOLE.dropdown = {};


SKIPOLE.dropdown.DropDown1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.dropdown.DropDown1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.dropdown.DropDown1.prototype.constructor = SKIPOLE.dropdown.DropDown1;


SKIPOLE.dropdown.SubmitDropDown1 = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    };
SKIPOLE.dropdown.SubmitDropDown1.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.dropdown.SubmitDropDown1.prototype.constructor = SKIPOLE.dropdown.SubmitDropDown1;
SKIPOLE.dropdown.SubmitDropDown1.prototype.eventfunc = function(e) {
    SKIPOLE.skiprefresh = true;
    // if action_json url set, call a json page
    let jsonurl = this.fieldvalues["url"];
    if (jsonurl) {
        // json url set, send data with a request for json and prevent default
        let self = this;
        let widgform = this.widg.find('form');
        let senddata = widgform.serializeArray();
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
    };
SKIPOLE.dropdown.SubmitDropDown1.prototype.setvalues = function (fieldlist, result) {
   if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    // sets hidden fields
    this.sethiddenfields(fieldlist, result);
    // sets hide
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
    };





SKIPOLE.dropdown.HiddenContainer = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.dropdown.HiddenContainer.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.dropdown.HiddenContainer.prototype.constructor = SKIPOLE.dropdown.HiddenContainer;
SKIPOLE.dropdown.HiddenContainer.prototype.setvalues = function (fieldlist, result) {
    if (!this.widg_id) {
        return;
        }
    let the_widg = this.widg;
    // check if hide
    let hidebox = this.fieldarg_in_result('hide', result, fieldlist);
    if (hidebox != undefined) {
        if (hidebox) {
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
    let button = the_widg.find("a");
    // get_field1
    let get_field1 = this.fieldarg_in_result('get_field1', result, fieldlist);
    if (get_field1 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field1", get_field1);
        button.attr('href', url);
        }
    // get_field2
    let get_field2 = this.fieldarg_in_result('get_field2', result, fieldlist);
    if (get_field2 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field2", get_field2);
        button.attr('href', url);
        }
    // get_field3
    let get_field3 = this.fieldarg_in_result('get_field3', result, fieldlist);
    if (get_field3 != undefined) {
        let href = button.attr('href');
        let url = this.setgetfield(href, "get_field3", get_field3);
        button.attr('href', url);
        }
    };
SKIPOLE.dropdown.HiddenContainer.prototype.eventfunc = function (e) {
    SKIPOLE.skiprefresh = true;
    // pressing close fades out the widget and prevents the link send
    let the_widg = this.widg;
    if (the_widg.is(":visible")) {
        the_widg.fadeOut('slow');
        }
    e.preventDefault();
    };




