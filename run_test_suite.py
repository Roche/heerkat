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
from unittest import TextTestRunner
from optparse import OptionParser


def get_test_name(test):
  splitted = str(test).split(' ')
  if len(splitted) > 1:
    return splitted[0]
  return str(test)

def log_result(result, monitored_output, detailed_output, test_suite):
  failed_tests = ', '.join(map(lambda (test, traceback): get_test_name(test), result.failures + result.errors))
  if not result.wasSuccessful():
    with open(monitored_output, "a") as log:
      log.write('FAILED [%s] detailed output: %s. Failed tests: %s.\n' % (test_suite, detailed_output, failed_tests))


def run_availability_tests(test_suite):
  __import__(test_suite)
  suite = unittest.TestLoader().loadTestsFromName(test_suite)
  runner = TextTestRunner(verbosity=4)
  result = runner.run(suite)
  return result


def parse_args():
  parser = OptionParser()
  parser.add_option('--detailed_output', nargs=1,
                    help='specify path where detailed logs can be found')
  parser.add_option('--monitored_output', nargs=1,
                    help='specify path where monitored logs can be found')
  parser.add_option('--test_suite', nargs=1, choices=['availability.service_tests',],
                    help='specify the test suite (python module) that you wish to execute')

  (options, args) = parser.parse_args()

  if not options.test_suite:   # Python 2.6 strikes again! Use argparse after Python upgrade
    parser.error('test_suite not given')
  if not options.monitored_output:
    parser.error('monitored_output not given')
  if not options.detailed_output:
    parser.error('detailed_output not given')

  return options


if __name__ == '__main__':
  args = parse_args()
  result = run_availability_tests(args.test_suite)
  log_result(result, args.monitored_output, args.detailed_output, args.test_suite)
