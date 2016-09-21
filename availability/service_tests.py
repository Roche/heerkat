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

    @skip(for_env='quickstart', message="Disabled by default. Plese setup all prerequisites")
    @timeout(60)
    @report('hbase', 'query-table')
    def test_hbase_querying(self):
        # when
        result = cmd('hbase shell -n %s' % hbase_query_script)

        # than
        self.assertEqual(0, result.exit_code, result.stderr)

    @skip(for_env='quickstart', message="Disabled by default. Please setup all prerequisites")
    @timeout(60)
    @report('hive', 'select-form-lifecycle_availability_test')
    def test_hive_querying(self):
        # when
        result = cmd('beeline -u "%s" -e "select * from availability_test.sample_data"' % connection_string_hive)

        # than
        self.assertEqual(0, result.exit_code, result.stderr)

    @skip(for_env="quickstart", message="Disabled by default. Please setup all prerequisites")
    @timeout(60)
    @report('impala', 'select-lifecycle.availability_test')
    def test_impala_querying(self):
        # when
        result = cmd('beeline -u "%s" -e "select * from availability_test.sample_data"' % connection_string_impala)

        # than
        self.assertEqual(0, result.exit_code, result.stderr)

    @skip(for_env="quickstart", message="Disabled by default. Please setup all prerequisites")
    @timeout(60)
    @report('solr', 'select-availability_test')
    def test_solr_querying(self):
        # when
        result = cmd('curl --negotiate -u: "http://%s/solr/availability_test/select?q=*:*"' % solr_instance)

        # than
        self.assertTrue('<int name="status">0</int>' in result.stdout, result.stderr)


    @timeout(60)
    @report('hue', 'hue-login-availability_test')
    def test_hue_login(self):
        # given
        self.get_hue_cookies(hue_cookies_file)
        csrftoken = self.get_csrftoken(hue_cookies_file)

        # when
        result = cmd('curl --data "username=%s&password=%s&next=/home&csrfmiddlewaretoken=%s" -b %s -Lkv %saccounts/login/' % (hue_login, hue_password, csrftoken, hue_cookies_file, hue_url))

        # than
        self.assertEqual(0, result.exit_code, result.stderr)
        self.assertTrue('HTTP/1.1 200 OK' in result.stderr, 'Login to Hue unsuccessful: %s' % result.stderr)

    def get_hue_cookies(self, file_for_cookies):
        cmd('rm -f %s' % file_for_cookies)
        cmd('curl -c %s -Lkv %s' % (file_for_cookies, hue_url)) # gets and saves session cookies

    def get_csrftoken(self, cookies_file):
        with open(cookies_file, 'r') as cookies:
            csrftoken_line = filter(lambda line: "csrftoken" in line, cookies)[0]
            csrftoken = csrftoken_line.split('\t')[6]
        return csrftoken.strip()