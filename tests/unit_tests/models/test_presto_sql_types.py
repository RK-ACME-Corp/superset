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

from unittest.mock import MagicMock

from superset.models.sql_types.presto_sql_types import (
    Array,
    Date,
    Interval,
    Map,
    Row,
    TimeStamp,
    TinyInteger,
)


def test_tiny_integer_python_type() -> None:
    t = TinyInteger()
    assert t.python_type is int


def test_tiny_integer_compiler_dispatch() -> None:
    visitor = MagicMock()
    assert TinyInteger._compiler_dispatch(visitor) == "TINYINT"


def test_interval_python_type() -> None:
    t = Interval()
    assert t.python_type is None


def test_interval_compiler_dispatch() -> None:
    visitor = MagicMock()
    assert Interval._compiler_dispatch(visitor) == "INTERVAL"


def test_array_python_type() -> None:
    t = Array()
    assert t.python_type is list


def test_array_compiler_dispatch() -> None:
    visitor = MagicMock()
    assert Array._compiler_dispatch(visitor) == "ARRAY"


def test_map_python_type() -> None:
    t = Map()
    assert t.python_type is dict


def test_map_compiler_dispatch() -> None:
    visitor = MagicMock()
    assert Map._compiler_dispatch(visitor) == "MAP"


def test_row_python_type() -> None:
    t = Row()
    assert t.python_type is None


def test_row_compiler_dispatch() -> None:
    visitor = MagicMock()
    assert Row._compiler_dispatch(visitor) == "ROW"


def test_timestamp_process_bind_param() -> None:
    dialect = MagicMock()
    result = TimeStamp.process_bind_param("2023-01-01 12:00:00", dialect)
    assert result == "TIMESTAMP '2023-01-01 12:00:00'"


def test_date_process_bind_param() -> None:
    dialect = MagicMock()
    result = Date.process_bind_param("2023-01-01", dialect)
    assert result == "DATE '2023-01-01'"


def test_timestamp_process_bind_param_with_timezone() -> None:
    dialect = MagicMock()
    result = TimeStamp.process_bind_param("2023-01-01 12:00:00+00:00", dialect)
    assert result == "TIMESTAMP '2023-01-01 12:00:00+00:00'"


def test_date_process_bind_param_different_format() -> None:
    dialect = MagicMock()
    result = Date.process_bind_param("2024-12-31", dialect)
    assert result == "DATE '2024-12-31'"
