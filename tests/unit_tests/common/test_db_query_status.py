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

from superset.common.db_query_status import QueryStatus


def test_query_status_values() -> None:
    assert QueryStatus.STOPPED == "stopped"
    assert QueryStatus.FAILED == "failed"
    assert QueryStatus.PENDING == "pending"
    assert QueryStatus.RUNNING == "running"
    assert QueryStatus.SCHEDULED == "scheduled"
    assert QueryStatus.SUCCESS == "success"
    assert QueryStatus.FETCHING == "fetching"
    assert QueryStatus.TIMED_OUT == "timed_out"


def test_query_status_is_str_enum() -> None:
    assert isinstance(QueryStatus.RUNNING, str)
    assert f"status={QueryStatus.RUNNING}" == "status=running"


def test_query_status_member_count() -> None:
    members = list(QueryStatus)
    assert len(members) == 8


def test_query_status_comparison() -> None:
    assert QueryStatus.SUCCESS == "success"
    assert QueryStatus.FAILED != "success"
