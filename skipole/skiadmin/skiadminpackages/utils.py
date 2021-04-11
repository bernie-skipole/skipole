
from ...ski.project_class_definition import SectionData


def clear_call_data(call_data, keep=None):
    "Clears call data apart from set of required values, and anything in the keep list"
    required = ['editedprojname',
                'editedprojurl',
                'editedprojversion',
                'editedprojbrief',
                'adminproj',
                'extend_nav_buttons',
                'caller_ident',
                'pagedata']
    if keep:
        if isinstance(keep, str) and (keep not in required):
            required.append(keep)
        else:
            # presume keep is a list of items
            for item in keep:
                if item not in required:
                    required.append(item)
    temp_storage = {key:value for key,value in call_data.items() if key in required}
    call_data.clear()
    call_data.update(temp_storage)



def formtextinput(pd, sectionalias, textblock_ref, field_label, input_text, **formvalues):
    """Provides a function to fill in the formtextinput section
       given an alias for the section, and the appropriate widget fields
       formvalues should be things like action=targetlabel, left_label='submit button label'"""

    sd = SectionData(sectionalias)
    sd['paratext', 'textblock_ref'] = textblock_ref
    sd['textinput', 'label'] = field_label
    sd['textinput', 'input_text'] = input_text

    # fill in form values
    for key, value in formvalues.items():
        sd['form', key] = value

    pd.update(sd)




