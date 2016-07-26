#!/usr/bin/env bash

#This script will create databases and users in non-protected environment. Please note, that for kerberized, secured
#environments you will need to adjust it accordingly


#Create hbase table and populate it. Check if data is available
#Create hive database and populate it with test table and data
#Make suere impala sees new table
#Create solr index and populate it with data


#Hbase
hbase shell -n resources/hbase/create_table