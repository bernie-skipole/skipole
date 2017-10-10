#######################################################################################
#
# TextBlocks are a mapping of the tuple (textref, language) to a block of text
#
# Various widgets that display TextBlocks are given a textref reference string, and
# the language is generally derived from a browser setting. The widget then obtains
# the block of text and displays it.
# 
# To obtain the text, the framework imports this module and creates an instance
# of the AccessTextBlocks object, and uses its methods to find the text.
#
# Therefore this module, and the AccessTextBlocks class must exist in your code.
#
# The example shown here can generally be left as it is. It reads TextBlocks from
# JSON files, stores them into memory and serves them to the framework when requested.
#
# The class also has methods for writing and saving TextBlocks to the JSON files
# which are used by skiadmin to create TextBlocks.
#
# However this class is placed here, rather than in the framework code, as your
# project may require TextBlocks to be sited elsewhere, such as in a database. If
# that is the case, you can re-write the AccessTextBlocks, but be sure to provide
# all the public attributes and methods of the original.
#
# Also be aware that if your web server creates multiple processes, then multiple
# instances AccessTextBlocks will be created.
#
########################################################################################


import os, json, shutil


_docutils_available = True
try:
    from docutils import core
except:
    _docutils_available = False



class AccessTextBlocks(object):


    def __init__(self, project, projectfiles, default_language):
        """The project imports this module and creates an instance of this class, and uses it to read the
           text of TextBlocks.
           As default, TextBlocks are stored in JSON files beneath the directory
           projectfiles/project/data/textblocks_json
           However if you wish to store them elsewhere, such as in a database somewhere, you can
           re-write this class.

           Doing so may make your project less portable, and editing textblocks with skiadmin
           may fail since it will depend on access to your database. You will probably need
           to populate your TextBlocks database yourself, independently of skiadmin. 

           A replacement class should have each of the public attributes and methods defined here
           that is, all the attributes and methods not starting with an underscore
        """

        # the self.default_language attribute is expected to exist
        self.default_language = default_language
        # as is a set of available languages
        self.languages = set()
 
        # this implementation holds all textblocks in memory in this dictionary of textblocks with keys
        # of the tuple (reference,language) and values being the text
        self._textblocks = {}
        # dictionary of textrefs with keys of reference and values being a list of languages for that textref
        self._textrefs = {}
        # read the json files from this directory and populate the above two dictionaries and self.languages
        self._textblocks_json_directory = os.path.join(projectfiles, project, "data", "textblocks_json")
        # for each language file in the directory, add it to the dictionary
        dir_contents = os.listdir(self._textblocks_json_directory)
        for filename in dir_contents:
            if not filename.endswith('.json'):
                continue
            filepath = os.path.join(self._textblocks_json_directory,filename)
            if not os.path.isfile(filepath):
                continue
            # filenames refer to languages, such as en.json, de.json
            language = filename[:-5].lower()
            self.languages.update([language])
            with open(filepath, 'r') as fp:
                textblocks_dict = json.load(fp)
                for textref, text in textblocks_dict.items():
                   self._textblocks[(textref,language)] = text
                   if textref in self._textrefs:
                       if language not in self._textrefs[textref]:
                           self._textrefs[textref].append(language)
                   else:
                        self._textrefs[textref] = [language]
        # sort language lists in self._textrefs
        for langlist in self._textrefs.values():
            langlist.sort()


    def get_textrefs(self):
        "Returns a list of the textrefs"
        return [textref for textref in self._textrefs]

    def get_textref_languages(self):
        "Return a dictionary {textref: [languages],...}"
        return self._textrefs.copy()

    def textref_exists(self, textref):
        "Return True if the textref exists"
        return textref in self._textrefs

    def get_exact_text(self, textref, language):
        "Get text with given textref and language, gets exact value, does not seek nearest, if not found return None"
        if (textref,language) in self._textblocks:
            return self._textblocks[(textref,language)]


    def get_decoded_text(self, textref, lang):
        """If the text of a Textblock is encoded in any special way, decode it here.
           this example decodes references ending with .rst as restructured text to html,
           it requires python3-docutils to be available, together with the docutils
           CSS html4css1.css file to be served"""
        text = self.get_text(textref, lang)
        if text is None:
            return
        if textref.endswith(".rst") and _docutils_available:
            # decode text as html
            parts = core.publish_parts(source=text, writer_name='html')
            return parts['html_body']
        else:
            return text


    def get_text(self, textref, lang):
        """Gets the text from the textblock, trying nearest language, returns None if not found
           lang is a tuple of preferred language, default_language"""
        if textref not in self._textrefs:
            return
        language, default_language = lang
        language = language.lower()
        default_language = default_language.lower()
        # try preferred language
        if (textref,language) in self._textblocks:
            return self.get_exact_text(textref,language)
        # if not preferred for example en-gb, try en
        shortlang = language.split('-')
        if (textref,shortlang[0]) in self._textblocks:
            return self.get_exact_text(textref,shortlang[0])
        # try default language
        if (textref,default_language) in self._textblocks:
            return self.get_exact_text(textref,default_language)
        shortlang = default_language.split('-')
        if (textref,shortlang[0]) in self._textblocks:
            return self.get_exact_text(textref,shortlang[0])
        # try self.default_language
        if (textref,self.default_language) in self._textblocks:
            return self.get_exact_text(textref,self.default_language)
        shortlang = self.default_language.split('-')
        if (textref,shortlang[0]) in self._textblocks:
            return self.get_exact_text(textref,shortlang[0])
        # try whatever language remains
        rlang = self.textrefs[textref][0]
        return self.get_exact_text(textref,rlang)

    def set_text(self, text, textref, language):
        """Sets the text into the textblock, with the given textref and language
           Used by skiadmin, in this implementation it is put into memory but
           not saved to the json files until the save method is called when the project
           is committed"""
        language = language.lower()
        if not text:
            self.del_text(textref, language)
            return
        self._textblocks[textref, language] = text
        self.languages.update([language])
        if textref in self._textrefs:
            langlist = self._textrefs[textref]
            if language not in langlist:
                langlist.append(language)
                langlist.sort()
        else:
            self._textrefs[textref] = [language]
        # if the language is of the format 'en-gb' then check if en is present, if not, add it
        shortlang = language.split('-')
        if shortlang[0] == language:
            return
        if (textref, shortlang) in self._textblocks:
            # A textblock with the given shortlang does exist, but check to see if it is just an empty string
            shortlangtext = self._textblocks[(textref, shortlang)]
            if (not shortlangtext) or (shortlangtext == " "):
                # add text
                self.set_text(text, textref, shortlang)
        else:
            # shortlang does not exist, so add it
            self.set_text(text, textref, shortlang)

    def del_text(self, textref, language):
        "Deletes the text from the textblock with the given language"
        language = language.lower()
        if (textref,language) not in self._textblocks:
            return
        del self._textblocks[(textref,language)]
        langlist = self._textrefs[textref]
        try:
            pos = langlist.index(language)
            del langlist[pos]
            if not langlist:
                del self._textrefs[textref]
        except:
            pass
        # test if language used anywhere
        for langlist in self._textrefs.values():
            if language in langlist:
                break
        else:
            self.languages.discard(language)

    def del_textblock(self, textref):
        "Deletes the textblock, all languages"
        langlist = self._textrefs[textref].copy()
        for language in langlist:
            self.del_text(textref, language)

    def copy(self, sourceref, destinationref):
        "Copies textblock"
        langlist = self._textrefs[sourceref]
        self._textrefs[destinationref] = []
        destlanglist = self._textrefs[destinationref]
        for language in langlist:
            self._textblocks[(destinationref, language)] = self._textblocks[(sourceref, language)]
            destlanglist.append(language)

    def save(self):
        "Creates json files from the textblocks"
        if os.path.isdir(self._textblocks_json_directory):
            # remove existing json files
            shutil.rmtree(self._textblocks_json_directory)
        os.mkdir(self._textblocks_json_directory)
        for language in self.languages:
            filepath = os.path.join(self._textblocks_json_directory, language + '.json')
            lang = (language, self.default_language)
            json_dict = {}
            for textref, langlist in self._textrefs.items():
                if language not in langlist:
                    continue
                json_dict[textref] = ''
                text = self.get_text(textref, lang)
                if text is not None:
                    json_dict[textref] = text
            # save the json dictionary to file
            with open(filepath, 'w') as fp:
                json.dump(json_dict, fp, indent=2, sort_keys=True)

    def get_reference_hierarchy(self):
        """Used to generate a list of nested dictionaries and lists
            by separating reference strings on the '.' character.
           returns a list of two elements:
               pos 0 is the list of top references - those without a dot
               pos 1 is a dictionary of lists, each list being of this same structure, having
               two elements.  Each dictionary key will be a name prior to the first dot."""
        reference_list = [self._textrefs.keys()]
        return self._make_hierarchy(reference_list)


    def _make_hierarchy(self, reference_list):
        """Recursive function used by get_reference_hierarchy
               reference_list should be a list of reference strings"""
        if not reference_list:
            return [[], {}]
        # unitstructure will be a list of strings with no . in them
        unit_structure = []
        for textref in reference_list:
            reflist = textref.split('.')
            if len(reflist) == 1:
                unit_structure.append(textref)
        for textref in unit_structure:
            reference_list.remove(textref)
        if not reference_list:
            return [unit_structure, {}]
        # any references still existing in reference_list must have more than one element
        # put first element as a dictionary key, with value a list of all sub reference strings
        temp_dict = {}
        for textref in reference_list:
            reflist = textref.split('.')
            if reflist[0] in temp_dict:
                temp_dict[reflist[0]].append('.'.join(reflist[1:]))
            else:
                temp_dict[reflist[0]] = ['.'.join(reflist[1:])]
        new_dict = {}
        for element, sublist in temp_dict.items():
            new_dict[element] = self._make_hierarchy(sublist)
        return [unit_structure, new_dict]

