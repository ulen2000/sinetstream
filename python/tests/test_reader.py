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

import time
import logging
import pytest

import sinetstream

logging.basicConfig(level=logging.ERROR)


service = 'service-1'
topic = 'mss-test-001'


def test_reader_1(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic) as f:
        pass
    assert True


def test_reader_1_list(dummy_reader_plugin):
    with sinetstream.MessageReader(service, [topic]) as f:
        pass
    assert True


def test_reader_2_list(dummy_reader_plugin):
    with sinetstream.MessageReader(service, [topic, topic+"2"]) as f:
        pass
    assert True


def test_reader_consistency_0(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, consistency=sinetstream.AT_MOST_ONCE) as f:
        pass
    assert True


def test_reader_consistency_1(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, consistency=sinetstream.AT_LEAST_ONCE) as f:
        pass
    assert True


def test_reader_consistency_2(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, consistency=sinetstream.EXACTLY_ONCE) as f:
        pass
    assert True


def test_reader_consistency_X(dummy_reader_plugin):
    try:
        with sinetstream.MessageReader(service, topic, consistency=999) as f:
            pass
    except sinetstream.InvalidArgumentError:
        assert True
    else:
        assert False


def test_reader_client_id_default(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic) as f:
        assert f.client_id is not None and f.client_id != ""
    assert True


def test_reader_client_id_empty(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, client_id="") as f:
        assert f.client_id is not None and f.client_id != ""
    assert True


def test_reader_client_id_set(dummy_reader_plugin):
    cid = "oreore"
    with sinetstream.MessageReader(service, topic, client_id=cid) as f:
        assert f.client_id == cid
    assert True


def test_reader_deser(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, value_deserializer=(lambda x: x)) as f:
        pass
    assert True


def test_reader_timeout(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, receive_timeout_ms=1000) as f:
        pass
    assert True


def test_reader_kafka_opt(dummy_reader_plugin):
    with sinetstream.MessageReader(service, topic, heartbeat_interval_ms=1000) as f:
        pass
    assert True


@pytest.mark.skip
def test_reader_timeout():
    tout = 100
    t1 = time.time()
    with sinetstream.MessageReader(service, topic,  receive_timeout_ms=tout) as f:
        for msg in f:
            assert False
    t2 = time.time()
    t = (t2 - t1) * 1000.0
    jitter_factor = 5
    assert t > tout / jitter_factor
    assert t < tout * jitter_factor
    assert True


@pytest.mark.skip
def test_reader_seek():
    with sinetstream.MessageReader(service, topic) as f:
        try:
            f.seek_to_beginning()
        except AssertionError:
            pass  # If any partition is not currently assigned, or if no partitions are assigned.
        try:
            f.seek_to_end()
        except AssertionError:
            pass  # If any partition is not currently assigned, or if no partitions are assigned.
    assert True