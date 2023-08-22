# -*- coding: utf-8 -*-
import re


def is_url(string):
    """ detect the string is an url or not """
    url_pattern = r'^(?:\w+:)?\/\/([^\s.]+\.\S{2}|localhost[:?\d]*)\S*$'
    return bool(re.match(url_pattern, string))


def is_base64(string):
    """ detect the string is a base64 or not """
    base64_pattern = r'^data:[A-Za-z0-9+/]+;base64,'
    return bool(re.match(base64_pattern, string))
