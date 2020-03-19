#!/usr/local/bin/python3.6
# vim: expandtab shiftwidth=4

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

import logging
import pytest

from sinetstream import MessageReader, MessageWriter, TEXT, BYTE_ARRAY
from conftest import SERVICE, TOPIC

logging.basicConfig(level=logging.ERROR)
pytestmark = pytest.mark.usefixtures('setup_config', 'dummy_reader_plugin', 'dummy_writer_plugin')


msgs = ['test message 001',
        'test message 002']

bmsgs = [x.encode() for x in msgs]


def test_thru():
    with MessageWriter(SERVICE, value_type=TEXT) as fw:
        for msg in msgs:
            fw.publish(msg)
    with MessageReader(SERVICE, value_type=TEXT) as fr:
        for expected, msg in zip(msgs, fr):
            assert msg.topic == TOPIC
            assert msg.value == expected


def test_enc_bin():
    with MessageWriter(SERVICE, value_type=BYTE_ARRAY, data_encryption=True) as fw:
        for msg in bmsgs:
            fw.publish(msg)
    with MessageReader(SERVICE, value_type=BYTE_ARRAY, data_encryption=True) as fr:
        for expected, msg in zip(bmsgs, fr):
            assert msg.topic == TOPIC
            assert msg.value == expected


def test_enc_text():
    with MessageWriter(SERVICE, value_type=TEXT, data_encryption=True) as fw:
        for msg in msgs:
            fw.publish(msg)

    with MessageReader(SERVICE, value_type=TEXT, data_encryption=True) as fr:
        for expected, msg in zip(msgs, fr):
            assert msg.topic == TOPIC
            assert msg.value == expected


@pytest.mark.parametrize(
    "crypto", [
        {"mode": "CBC",        "padding": "pkcs7"},
        {"mode": "CFB",        "padding": "none"},
        {"mode": "OFB",        "padding": "none"},
        {"mode": "CTR",        "padding": "none"},
        {"mode": "OPENPGP",    "padding": "none"},
        {"mode": "OPENPGPCFB", "padding": "none"},
        {"mode": "EAX",        "padding": "none"},
        {"mode": "GCM",        "padding": "none"},
    ])
def test_enc_mode(crypto):
    with MessageWriter(SERVICE, value_type=TEXT, data_encryption=True, crypto=crypto) as fw:
        for msg in msgs:
            fw.publish(msg)
    with MessageReader(SERVICE, value_type=TEXT, data_encryption=True, crypto=crypto) as fr:
        for expected, msg in zip(msgs, fr):
            assert msg.topic == TOPIC
            assert msg.value == expected


@pytest.fixture()
def config_params():
    return {
        'crypto': {
            'algorithm': 'AES',
            'key_length': 128,
            'mode': 'GCM',
            'padding': 'none',
            'key_derivation': {
                'algorithm': 'pbkdf2',
            },
            'salt_bytes': 16,
            'iteration': 10000,
            'password': {
                'value': 'secret-000',
            },
        },
        'data_encryption': True,
    }
