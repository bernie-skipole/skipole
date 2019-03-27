

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
    // if action_json url set, call a json page
    var jsonurl = this.fieldvalues["url"];
    if (jsonurl) {
        // json url set, send data with a request for json and prevent default
        var self = this;
        var widgform = this.widg.find('form');
        var senddata = widgform.serializeArray();
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
                              alert(errorThrown);
                              }
                  });
        }
    };
SKIPOLE.dropdown.SubmitDropDown1.prototype.setvalues = function (fieldlist, result) {
    /* This widget accepts fields - hide */
   if (!this.widg_id) {
        return;
        }
    var the_widg = this.widg;
    var set_hide = this.fieldarg_in_result('hide', result, fieldlist);
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

