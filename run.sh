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

export PYTHONUNBUFFERED=1

NOW=$(date +%Y-%m-%d:%H:%M:%S)
DETAILED_LOG="log/output_${NOW}.log"
MONITORED_LOG="log/execution.log"
USER=${TEST_USER:-cloudera}

python run_test_suite.py --detailed_output ${DETAILED_LOG} --monitored_output ${MONITORED_LOG} --test_suite $1 > ${DETAILED_LOG} 2>&1
