/*
####### SKIPOLE WEB FRAMEWORK #######

 paths-0.1.0.js  - javascript validators

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

A javascript client-side validator is defined here for each of the python
server-side validators in module paths.py.  These javascript validators
are designed to support the server side validators, and improve the user
experience, but are not necessarily as rigorous.  Anything getting past
these, will then be tested by the server-side validators.

Call a validator function using
result = SKIPOLE.paths.testname(item, allowed_values, args);

Where testname is the python validator class name

item: is the input string being tested

allowed_values: an array of allowed strings

args: an object of further parameters depending on the validator

The function returns true if the test passes and is validated, false otherwise.

*/


SKIPOLE.paths = {
    /* Fail if no allowed values given, otherwise item must be in allowed values */

    /* no op */
    PathLeadingTrailingSlashes: function (item, allowed_values, args) {
        return true;
    },
    /* no op */
    IdentExists: function (item, allowed_values, args) {
        return true;
    },
    /* no op */
    NameNotInFolder: function (item, allowed_values, args) {
        return true;
    }
}



