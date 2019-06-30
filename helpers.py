import os
import sys

def formatname(name):
    """ Takes the given initials and formats to uppercase """

    upper = ""

    if len(name) is not 3:
        return None
    elif not name.isalpha():
        return None
    else:
        return name.upper()

