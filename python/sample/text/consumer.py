# Copyright (C) 2019 National Institute of Informatics
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import argparse

import sinetstream

parser = argparse.ArgumentParser(description="SINETStream Consumer")
parser.add_argument("-s", "--service",
                    metavar="SERVICE_NAME",
                    required=True)
parser.add_argument("-t", "--topic",
                    metavar="TOPIC",
                    action="append",
                    required=True)

args = parser.parse_args()

print(f"# service={args.service}")
print(f"# topics={','.join(args.topic)}")

with sinetstream.MessageReader(args.service, args.topic) as f:
    for msg in f:
        try:
            value = msg.value.decode('utf-8')
            print(f"topic={msg.topic} value(utf-8)='{value}'")
        except:
            print(f"topic={msg.topic} value({type(msg.value).__name__})={msg.value}")