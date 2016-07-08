# Heerkat - Hadoop Cluster Monitoring Bundle 

Hadoop Cluster Monitoring Bundle helps to diagnose the state of services in a Hadoop cluster. We made it work with the Cloudera QuickStart VM, so you can evaluate it easily. However, it was designed to work with production clusters and this is how it is utilized by us.

Heerkat is available under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## General Requirements: 	

- create a 'log' directory in the root folder to store the log files (the output paths for the tests can be set in `run.sh` - variables `DETAILED_LOG` and `MONITORED_LOG`)
- set an environment variable to indicate that the Cloudera QuickStart installation is used: `export EXECUTION_ENV=quickstart`

## Availability monitoring 

Availability monitoring is performed with custom scripts written in Python. Python code periodically (needs to be setup in Cron or other scheduler) executes the checks for chosen Hadoop components and logs predefined 'failure line' to a file. This file can be monitored by the end-users or with a preferred monitoring system, e.g. NetIQ App Manager.
 
### Running tests

This code should work with the Cloudera QuickStart. To run the test simply execute:

    ./run.sh availability.service_tests
    
### Skipping a test 

There is a decorator @skip(for_env=None, message='') that can be used to disable test or tests for a given environment.  

### Requirements

Most of the test will work out of the box on Cloudera Quickstart installation. Below you will find instructions if any test needs configuration adjustment.


### Oozie workflow test requirements

To test the Oozie workflow the node from which you run the test needs to be whitelisted  in Cloudera Manager. 

- Go into Oozie configuration and edit "Oozie Server Advanced Configuration Snippet (Safety Valve) for oozie-site.xml". For Cloudera Quickstart paste in: 

```
<property>
<name>oozie.service.HadoopAccessorService.nameNode.whitelist</name>
<value/>
<description/>
</property>

<property>
<name>oozie.service.HadoopAccessorService.jobTracker.whitelist</name>
<value/>
<description>
Whitelisted job tracker for Oozie service.
</description>
</property>
```
- Go into HDFS configuation and edit "Cluster-wide Advanced Configuration Snippet (Safety Valve) for core-site.xml". For Cloudera Quickstart pase in:

```
<property> 
<name>hadoop.proxyuser.oozie.hosts</name> 
<value>*</value> 
</property> 
<property> 
<name>hadoop.proxyuser.oozie.groups</name> 
<value>*</value> 
</property>
```

# Features

This bundle will run the following tests:
 - a simple Pi estimator MR job from Hadoop examples, using 5 mappers and 5 reducers.
 - hdfs file operations (copy to hdfs, read from hdfs)
 - spark application execution
 - pig application execution
 - oozie workflow
 

