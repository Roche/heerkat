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


from utils.properties import *


def skip(for_env=None, message=''):
  def decorate(function):
    env = get_environment()
    if for_env is None or for_env == env:
      print "Skipping test (%s) with message: %s." % (function.func_name, message)
      return empty
    return function

  def empty(*args, **kwargs):
    pass

  return decorate
