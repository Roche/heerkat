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

import unittest


from utils.skip import *
from utils.timeout import *
import re



class ServiceTest(unittest.TestCase):

    @timeout(180)
    @report('mapreduce', 'PiEstimator')
    def test_mr_application_execution(self):
        # when
        result = cmd('hadoop jar %s pi 5 5' % mr_examples_jar)

        # than
        self.assertEqual(0, result.exit_code, result.stderr)

    @timeout(60)
    @report('hdfs', 'write-read-rm')
    def test_hdfs_write_and_read(self):
        #given
        cmd('hdfs dfs -mkdir -p ' + destination_path)
        destination_file = destination_path + 'hdfs_test_data'

        #when
        write_result = cmd('hdfs dfs -put %s %s' % (sample_data, destination_file))
        read_result = cmd('hdfs dfs -cat ' + destination_file)
        rm_result = cmd('hdfs dfs -rm ' + destination_file)

        #than
        self.assertEqual(0, write_result.exit_code, write_result.stderr)
        self.assertEqual(0, read_result.exit_code, read_result.stderr)
        self.assertEqual(0, rm_result.exit_code, rm_result.stderr)


    @timeout(180)
    @report('spark', 'SparkPi')
    def test_spark_application_execution(self):
        # when
        result = cmd(
            'spark-submit --class org.apache.spark.examples.SparkPi %s %s 10' % (spark_properties, spark_examples_jar))

        # than
        self.assertEqual(0, result.exit_code, result.stderr)

    @timeout(180)
    @report('pig', 'wordcount')
    def test_pig_application_execution(self):
        # given
        cmd('hdfs dfs -mkdir -p ' + destination_path)
        destination_file = destination_path + 'pig_test_data'
        cmd('hdfs dfs -put %s %s' % (sample_data, destination_file))

        # when
        result = cmd('''pig -e "A = load '%s'; \
          B = foreach A generate flatten(TOKENIZE((chararray)$0)) as word; \
          C = group B by word; \
          D = foreach C generate COUNT(B), group; \
          dump D;" ''' % destination_file)

        # than
        self.assertEqual(0, result.exit_code, result.stderr)


    @timeout(360)
    @report('oozie', 'streaming-action')
    def test_oozie_workflow(self):
        # given
        input_data_dir = 'test/availability/input-data'
        apps_streaming_dir = 'test/availability/apps/streaming'

        cmd('hdfs dfs -rm -r %s' % input_data_dir)
        cmd('hdfs dfs -mkdir -p %s' % input_data_dir)
        cmd('hdfs dfs -put %s %s' % (sample_data, input_data_dir))

        cmd('hdfs dfs -rm -r %s' % apps_streaming_dir)
        cmd('hdfs dfs -mkdir -p %s' % apps_streaming_dir)
        cmd('hdfs dfs -put resources/oozie/workflow.xml %s' % apps_streaming_dir)


        # when
        result = cmd('oozie job -oozie %s -config resources/oozie/job.properties -run' % oozie_host)
        job_id = result.stdout.replace('job: ', '')
        cmd('oozie job -oozie %s -poll %s -interval 1' % (oozie_host, job_id))
        result = cmd('oozie job -oozie %s -info %s' % (oozie_host, job_id))

        # than
        status = re.search('Status\s+:\s+(.+)', result.stdout).group(1)
        self.assertEqual('SUCCEEDED', status, result.stderr)
