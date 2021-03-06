#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import traceback
import re
import json
import os
import multiprocessing

import logging

from nose import case

LOG = logging.getLogger(__name__)


def parse_json_file(file_path):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    commands_path = os.path.join(
        current_directory, file_path)
    with open(commands_path, 'r') as f:
        return json.load(f)


def get_exc_message(exception_value):
    """
    @exception_value - Exception type object
    """
    _exc_long = str(exception_value)
    if isinstance(_exc_long, basestring):
        return _exc_long.split('\n')[0]
    return u""


def get_description(test_obj):
    '''
    Parses docstring of test object in order
    to get necessary data.

    test_obj.test._testMethodDoc is using directly
    instead of calling test_obj.shortDescription()
    for the sake of compability with python 2.6 where
    this method works pretty buggy.
    '''
    if isinstance(test_obj, case.Test):
        docstring = test_obj.test._testMethodDoc

        if docstring:
            duration_pattern = r'Duration:.?(?P<duration>.+)'
            duration_matcher = re.search(duration_pattern, docstring)

            if duration_matcher:
                duration = duration_matcher.group(1)
                docstring = docstring[:duration_matcher.start()]
            else:
                duration = None
            docstring = docstring.split('\n')
            name = docstring.pop(0)
            description = u'\n'.join(docstring) if docstring else u""

            return name, description, duration
    return u"", u"", u""


def modify_test_name_for_nose(test_path):
    test_module, test_class, test_method = test_path.rsplit('.', 2)
    return '{0}:{1}.{2}'.format(test_module, test_class, test_method)


def format_exception(exc_info):
    ec, ev, tb = exc_info

    # formatError() may have turned our exception object into a string, and
    # Python 3's traceback.format_exception() doesn't take kindly to that (it
    # expects an actual exception object).  So we work around it, by doing the
    # work ourselves if ev is a string.
    if isinstance(ev, basestring):
        tb_data = ''.join(traceback.format_tb(tb))
        return tb_data + ev
    else:
        return ''.join(traceback.format_exception(*exc_info))


def format_failure_message(message):
    message = get_exc_message(message)
    matcher = re.search(
        r'^[a-zA-Z]+\s?(\d+)\s?[a-zA-Z]+\s?[\.:]\s?(.+)',
        message)
    if matcher:
        step, msg = matcher.groups()
        return int(step), msg
    return None, message


def run_proc(func, *args):
    proc = multiprocessing.Process(
        target=func,
        args=args)
    proc.daemon = True
    proc.start()
    return proc


def get_module(module_path):
    pass
