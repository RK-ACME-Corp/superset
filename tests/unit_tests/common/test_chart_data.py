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

from superset.common.chart_data import ChartDataResultFormat, ChartDataResultType


def test_chart_data_result_format_values() -> None:
    assert ChartDataResultFormat.CSV == "csv"
    assert ChartDataResultFormat.JSON == "json"
    assert ChartDataResultFormat.XLSX == "xlsx"


def test_chart_data_result_format_table_like() -> None:
    table_like = ChartDataResultFormat.table_like()
    assert ChartDataResultFormat.CSV in table_like
    assert ChartDataResultFormat.XLSX in table_like
    assert ChartDataResultFormat.JSON not in table_like


def test_chart_data_result_format_table_like_is_set() -> None:
    table_like = ChartDataResultFormat.table_like()
    assert isinstance(table_like, set)
    assert len(table_like) == 2


def test_chart_data_result_type_values() -> None:
    assert ChartDataResultType.COLUMNS == "columns"
    assert ChartDataResultType.FULL == "full"
    assert ChartDataResultType.QUERY == "query"
    assert ChartDataResultType.RESULTS == "results"
    assert ChartDataResultType.SAMPLES == "samples"
    assert ChartDataResultType.TIMEGRAINS == "timegrains"
    assert ChartDataResultType.POST_PROCESSED == "post_processed"
    assert ChartDataResultType.DRILL_DETAIL == "drill_detail"


def test_chart_data_result_format_is_str_enum() -> None:
    assert isinstance(ChartDataResultFormat.CSV, str)
    assert f"format={ChartDataResultFormat.CSV}" == "format=csv"


def test_chart_data_result_type_is_str_enum() -> None:
    assert isinstance(ChartDataResultType.FULL, str)
    assert f"type={ChartDataResultType.FULL}" == "type=full"


def test_chart_data_result_format_members() -> None:
    members = list(ChartDataResultFormat)
    assert len(members) == 3


def test_chart_data_result_type_members() -> None:
    members = list(ChartDataResultType)
    assert len(members) == 8
