from factorycore_utils.string_helpers import Case, convert_case
from functools import reduce
import json

class factory_dict(dict):
    
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
    
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def __getattr__(self, attr):
        def _traverse(obj, attr):
            if self._is_indexable(obj):
                try:
                    return obj[int(attr)]
                except:
                    return None
            elif isinstance(obj, dict):
                return obj.get(attr, None)
            else:
                return None
        if '.' in attr:
            return reduce(_traverse, attr.split('.'), self)
        return self.get(attr, None)

    def _wrap(self, value):
        if self._is_indexable(value):
            # (!) recursive (!)
            return type(value)([self._wrap(v) for v in value])
        elif isinstance(value, dict):
            return factory_dict(value)
        else:
            return value
    
    @staticmethod
    def _is_indexable(obj):
        return isinstance(obj, (tuple, list, set, frozenset))


def search_dictionary(dict_to_search, search_key, value_to_return_if_not_found = None, convert_to_case: Case = Case.NO_CONVERSION):
    """
    Do a lookup of a Dictionary and return the Value for the search Key.
    If search_key does not exist in the Dictionary, return value_to_return_if_not_found.

    Parameters:
    dict_to_search - Dictionary object (containing key/value pairs) to search.
    search_key - Key to search for in dict.  Case-sensitive.
                 Dot-notation applies as follows:
                   - dict_to_search = {
                                        "Name": "Test",
                                        "Values": {
                                                    "Title": "Results",
                                                    "Results":  [
                                                                  {
                                                                    "Definition": "Core Sample",
                                                                    "Outcome": "Prospective"
                                                                  },
                                                                  {
                                                                    "Definition": "Follow-up",
                                                                    "Outcome": "For review"
                                                                  }
                                                                ]
                                                  }
                                      }
                    - Valid searches include: 
                        Name (returns 'Test)
                        Values.Title (returns 'Results')
                        Values.Results.0 (returns { "Definition": "Core Sample", "Outcome": "Prospective })
                        Values.Results.1.Definition (returns 'Follow-up')
                    - Note that the search_key is case-sensitive.  Also note how array elements are specified (see second search example in the line above).
                            
    value_to_return_if_not_found - If no item is found, return this value.  Default None.
    convert_to_case - Enum specifying how the found Value will be converted.  Default NO_CONVERSION.
    """

    result = None

    if "." in search_key:
        result = getattr(factory_dict(dict_to_search), search_key)
    else:
        for k, v in dict_to_search.items():
            if k.casefold() == search_key.casefold():
                result = v
                break

    if result is None:
        result = value_to_return_if_not_found

    if isinstance(result, str):
        result = convert_case(result.strip(), convert_to_case)

    return result


def search_dictionary_orig(dict, search_key, value_to_return_if_not_found=None, convert_to_case: Case = Case.NO_CONVERSION):
    # Do a case-insensitive lookup of a Dictionary and return the Value for the search Key.
    # If search_key does not exist in the Dictionary, return value_to_return_if_not_found.

    # Parameters:
    # dict - Dictionary object (containing key/value pairs) to search
    # search_key - Key to search for in dict.  Case is unimportant.
    # value_to_return_if_not_found - If no item is found, return this value.  Default None.
    # convert_to_case - Enum specifying how the found Value will be converted.  Default NO_CONVERSION.

    result = value_to_return_if_not_found

    for k, v in dict.items():
        if k.lower() == search_key.lower():
            if isinstance(v, str):
                result = convert_case(v.strip(), convert_to_case)
            else:
                result = v

            break

    return result
