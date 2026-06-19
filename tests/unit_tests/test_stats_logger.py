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

from superset.stats_logger import BaseStatsLogger, DummyStatsLogger


def test_base_stats_logger_key_with_prefix() -> None:
    logger = BaseStatsLogger(prefix="myapp")
    assert logger.key(".metric") == "myapp.metric"


def test_base_stats_logger_key_without_prefix() -> None:
    logger = BaseStatsLogger(prefix="")
    assert logger.key("metric") == "metric"


def test_base_stats_logger_default_prefix() -> None:
    logger = BaseStatsLogger()
    assert logger.prefix == "superset"
    assert logger.key(".count") == "superset.count"


def test_base_stats_logger_incr_not_implemented() -> None:
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.incr("metric")


def test_base_stats_logger_decr_not_implemented() -> None:
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.decr("metric")


def test_base_stats_logger_timing_not_implemented() -> None:
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.timing("metric", 1.0)


def test_base_stats_logger_gauge_not_implemented() -> None:
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.gauge("metric", 1.0)


def test_dummy_stats_logger_incr(caplog: pytest.LogCaptureFixture) -> None:
    dummy = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        dummy.incr("test.metric")
    assert "test.metric" in caplog.text


def test_dummy_stats_logger_decr(caplog: pytest.LogCaptureFixture) -> None:
    dummy = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        dummy.decr("test.metric")
    assert "test.metric" in caplog.text


def test_dummy_stats_logger_timing(caplog: pytest.LogCaptureFixture) -> None:
    dummy = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        dummy.timing("test.metric", 42.5)
    assert "test.metric" in caplog.text
    assert "42.5" in caplog.text


def test_dummy_stats_logger_gauge(caplog: pytest.LogCaptureFixture) -> None:
    dummy = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        dummy.gauge("test.metric", 99.9)
    assert "test.metric" in caplog.text
