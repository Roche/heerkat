# Heerkat - Hadoop Cluster Monitoring Bundle 

Hadoop Cluster Monitoring Bundle helps to diagnose the state of services in a Hadoop cluster. We made it work with the Cloudera QuickStart VM, so you can evaluate it easily. However, it was designed to work with production clusters and this is how it is utilized by us.

Heerkat is available under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Requirements: 	

- create 'log' directory for storing logs in the root folder (the output paths for the tests can be set in `run.sh` - variables `DETAILED_LOG` and `MONITORED_LOG`)
- set an environment variable to indicate that the Cloudera QuickStart installation is used: `export EXECUTION_ENV=quickstart`

## Availability monitoring 

Availability monitoring is performed with custom scripts written in Python. Python code periodically (needs to be setup in Cron or other scheduler) executes the checks for chosen Hadoop components and logs predefined 'failure line' to a file. This file can be monitored by the end-users or with a preferred monitoring system, e.g. NetIQ App Manager.
 
### Running tests

This code should work with the Cloudera QuickStart installation without any modifications. To run the test simply execute:

    ./run.sh availability.service_tests

This test will run:
 - a simple Pi estimator MR job from Hadoop examples, using 5 mappers and 5 reducers.
 - test hdfs file operations (copy to hdfs, read from hdfs)
 