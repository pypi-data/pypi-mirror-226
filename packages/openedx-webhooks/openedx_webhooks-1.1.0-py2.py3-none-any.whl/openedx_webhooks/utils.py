"""
Utilities used by Open edX Events Receivers.
"""
import json
import logging
from collections.abc import MutableMapping

import requests
from opaque_keys.edx.locator import CourseLocator

logger = logging.getLogger(__name__)


def fix_dict_keys(d: dict):
    """
    Remove dict keys from a dict.

    This fixes a problem with course objects, for which vars(course) or course.__dict__ return a dict
    which contains dicts as keys, and are therefore not json serializable.
    We convert these dicts in place of keys, to their str representation.
    """
    # Initialize the response
    r = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = fix_dict_keys(v)
        if type(k) not in [str, int, float]:
            r[str(k)] = v
        else:
            r[k] = v
    return r


def send(url, payload, www_form_urlencoded: bool = False):
    """
    Dispatch the payload to the webhook url, return the response and catch exceptions.
    """
    if www_form_urlencoded:
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        payload = flatten_dict(payload)
    else:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    r = requests.post(url, data=json.dumps(payload, default=str), headers=headers, timeout=10)

    return r


def flatten_dict(dictionary, parent_key="", sep="_"):
    """
    Generate a flatten dictionary-like object.

    Taken from:
    https://stackoverflow.com/a/6027615/16823624
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, str(value)))
    return dict(items)


def serialize_course_key(inst, field, value):  # pylint: disable=unused-argument
    """
    Serialize instances of CourseLocator.

    When value is anything else returns it without modification.
    """
    if isinstance(value, CourseLocator):
        return str(value)
    return value
