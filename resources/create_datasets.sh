#!/usr/bin/env bash

# *******************************************************************************
# * Copyright © 2016 Hoffmann-La Roche
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *   http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *******************************************************************************

#This script will create databases and users in non-protected environment. Please note, that for kerberized, secured
#environments you will need to adjust it accordingly


#Create hbase table and populate it. Check if data is available
#Create hive database and populate it with test table and data
#Make suere impala sees new table
#Create solr index and populate it with data


#Hbase
hbase shell -n hbase/create_table