from re import sub
from enum import Enum


class Case(Enum):
    NO_CONVERSION = 1
    SNAKE_CASE = 2
    TITLE_CASE = 3
    UPPER_CASE = 4
    LOWER_CASE = 5


def to_snake_case(s):
    return '_'.join(
        sub('([A-Z]+)', r' \1',
            sub('([A-Z]+)([A-Z][a-z]+)', r'\1 \2',
                sub('_([A-Z]+)', r' \1',
                    s.replace('-', ' ')))).split()).lower()


def to_title_case(s):
    exceptions = ["and", "or", "the", "a", "of", "in"]
    lowercase_words = to_snake_case(s).split("_")
    final_words = [lowercase_words[0].capitalize()]
    final_words += [word if word in exceptions else word.capitalize() for word in lowercase_words[1:]]
    return " ".join(final_words)


def convert_case(s, case_type: Case):
    result = ""

    if case_type is Case.SNAKE_CASE:
        result = to_snake_case(s)
    elif case_type is Case.TITLE_CASE:
        result = to_title_case(s)
    elif case_type is Case.UPPER_CASE:
        result = s.upper()
    elif case_type is Case.LOWER_CASE:
        result = s.lower()
    else:
        result = s

    return result


def delimited_string_to_list(s, delimiter=",", case_type: Case = Case.NO_CONVERSION):
    # Return a list comprising each element of a delimited string

    # Parameters:
    # s - Delimited string
    # delimiter - Delimiter of the string. Default comma.
    # case_type - Enum of the Case to convert each element to. Default NO_CONVERSION.

    return [convert_case(i.strip(), case_type) for i in s.split(delimiter) if i]


def list_to_delimited_string(list, delimiter=","):
    # Return a delimited string of list items

    # Parameters:
    # list - The List to generate the delimited string from
    # delimiter - Delimiter of the string. Default comma.

    return delimiter.join(list)


def remove_illegal_parquet_characters_from_delimited_string(str, delimiter=None):
    # In line with Parquet naming restrictions, remove illegal characters and replace spaces with an underscore

    # Parameters:
    # s - String to correct
    # delimiter - Delimiter used in String.  Default None.

    illegal_characters_re = r'[()";{}\n\t=-]'

    if delimiter is None:
        result = "_".join(sub(illegal_characters_re, "", str.strip()).split())
    else:
        result = delimiter.join(["_".join(sub(illegal_characters_re, "", i.strip()).split()) for i in str.split(delimiter) if i])

    return result


def remove_html_tags(text, replacement=''):
    """Remove html tags from a string"""
    return sub('<.*?>', replacement, text).strip().replace('  ', ' ')
