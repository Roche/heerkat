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

import shlex
import time

from subprocess import Popen, PIPE


class Result:
    pass


def cmd(command):
    result = Result()

    p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()

    result.exit_code = p.returncode
    result.stdout = stdout
    result.stderr = stderr
    result.command = command

    if p.returncode != 0:
        print 'Error executing command [%s]' % command
        print 'stderr: [%s]' % stderr
        print 'stdout: [%s]' % stdout

    return result


def cmd_test(command, num_retries, back_off, exit_pattern_stdout):
    count = 0

    while count < num_retries:
        result = cmd(command)
        check = exit_pattern_stdout in result.stdout
        if check == True:
            break
        count += 1
        time.sleep(back_off)

    return [check, result.stdout]
