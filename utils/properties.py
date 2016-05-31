# -*- coding: utf-8 -*-
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

import time
import os
import glob

# TODO: Old python strikes again! No enums for us in Python 2.6.6 ...
QUICKSTART = 'quickstart'


def get_environment():
    env_name = os.environ['EXECUTION_ENV']
    if env_name not in [QUICKSTART]:
        raise ValueError('Given environment (%s) is not supported.' % env_name)
    return env_name


def environment_dependent(quickstart):
    env = get_environment()
    if env == QUICKSTART:
        return quickstart


# TODO: avoid hardcoding CDH version. For Cloudera QuickStart there is one path. For all parcel based installations, we need to think how to address this issue.
mr_examples_jar = environment_dependent(
    quickstart='/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar',
)
spark_examples_jar = environment_dependent(
    quickstart= glob.glob("/usr/lib/spark/lib/spark-examples-*.jar")[0]
)
oozie_host = environment_dependent(
    quickstart = 'localhost 9090'
)



spark_properties = '--num-executors 3 --driver-memory 512m --executor-memory 512m --executor-cores 1 --master yarn-client'


# return codes
assertion_success_code = 0
assertion_failure_code = 1
timeout_expired_code = 2

sample_data = 'resources/sample_data'
destination_path = '/tmp/cluster_monitoring/%s' % time.time()
