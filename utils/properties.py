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


#Map Reduce
mr_examples_jar = environment_dependent(
    quickstart='/usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar',
)

#Spark
spark_examples_jar = environment_dependent(
    quickstart= glob.glob("/usr/lib/spark/lib/spark-examples-*.jar")[0],
)
spark_properties = '--num-executors 3 --driver-memory 512m --executor-memory 512m --executor-cores 1 --master yarn-client'

#Oozie
oozie_host = environment_dependent(
    quickstart = 'http://quickstart.cloudera:11000/oozie',
)

#Hbase (please check if the following is true for your environment)
hbase_thrift_classpath = '/usr/lib/hbase/lib/libthrift-0.9.0.jar:/usr/lib/hbase/hbase-thrift.jar:/usr/lib/hbase/lib/slf4j-api-1.7.5.jar:/usr/lib/hbase/lib/httpcore-4.2.5.jar:/usr/lib/hbase/hbase-client.jar'
#hbase_query_script = 'resources/hbase/query'
hbase_thrift_server = environment_dependent(
  quickstart='http://quicstart.cloudera 9090',
)
hbase_query_script = 'resources/hbase/query_table'

#Hive settings
connection_string_hive = environment_dependent(
  quickstart='jdbc:hive2://quickstart.cloudera:10000',
)

#Impala settings
connection_string_impala = environment_dependent(
  quickstart='jdbc:hive2://quickstart.cloudera:10000',
)

#Solr
solr_instance = environment_dependent(
    quickstart='quickstart.cloudera:8983'
)

#HUE
hue_login='cloudera'
# following property is overridden during bamboo deployment,
# if you need to change this property, please change deployment plan as well
hue_password='cloudera'
hue_cookies_file='hue_cookies'
hue_url = environment_dependent(
  quickstart='http://quickstart.cloudera:8888/',

)

#Zookeeper
zookeeper_hosts = environment_dependent(
  quickstart=['quickstart.cloudera'],
)

# return codes
assertion_success_code = 0
assertion_failure_code = 1
timeout_expired_code = 2

sample_data = 'resources/sample_data'
destination_path = '/tmp/cluster_monitoring/%s' % time.time()
