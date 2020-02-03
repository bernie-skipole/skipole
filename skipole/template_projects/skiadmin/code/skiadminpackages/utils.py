

import html

from skipole import FailPage, ServerError
from skipole import skilift


def clear_call_data(call_data, keep=None):
    "Clears call data apart from set of required values, and anything in the keep list"
    required = ['editedprojname',
                'editedprojurl',
                'editedprojversion',
                'editedprojbrief',
                'adminproj',
                'extend_nav_buttons',
                'caller_ident']
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


