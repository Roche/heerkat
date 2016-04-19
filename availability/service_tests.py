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

import unittest


from utils.skip import *
from utils.timeout import *



class ServiceTest(unittest.TestCase):

  @timeout(180)
  @report('mapreduce', 'PiEstimator')
  def test_mr_application_execution(self):
    # when
    result = cmd('hadoop jar %s pi 5 5' % mr_examples_jar)

    # than
    self.assertEqual(0, result.exit_code, result.stderr)

