"""
 *******************************************************************************
 * Copyright © 2016 Hoffmann-La Roche
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************
"""

from properties import *
from command import *

import traceback
import signal
import sys


class TimeoutError(AssertionError):
    pass


def timeout(timeout_seconds):
    def decorate(function):
        message = "Timeout (%s sec) elapsed for test %s" % (timeout_seconds, function.__name__)

        def handler(signum, frame):
            raise TimeoutError(message)

        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout_seconds)
            try:
                function_result = function(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
            return function_result

        new_f.func_name = function.func_name
        return new_f

    return decorate


def report(service, testcase):
    def decorate(function):

        def get_result(code, message=None):
            result = Result()
            result.exit_code = code
            result.stderr = message
            result.command = None
            return result

        def new_f(*args, **kwargs):
            try:
                function_result = function(*args, **kwargs)

            except AssertionError:
                error_type, error_message, error_traceback = sys.exc_info()
                raise

            return function_result

        new_f.func_name = function.func_name
        return new_f

    return decorate
