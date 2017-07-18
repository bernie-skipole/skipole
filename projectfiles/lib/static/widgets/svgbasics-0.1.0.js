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



SKIPOLE.svgbasics.SimpleText = function (widg_id, error_message, fieldmap) {
    SKIPOLE.BaseWidget.call(this, widg_id, error_message, fieldmap);
    this.display_errors = false;
    };
SKIPOLE.svgbasics.SimpleText.prototype = Object.create(SKIPOLE.BaseWidget.prototype);
SKIPOLE.svgbasics.SimpleText.prototype.constructor = SKIPOLE.svgbasics.SimpleText;





