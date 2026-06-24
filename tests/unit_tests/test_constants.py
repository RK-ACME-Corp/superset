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

from superset.constants import (
    CHANGE_ME_SECRET_KEY,
    EMPTY_STRING,
    EXAMPLES_DB_UUID,
    EXTRA_FORM_DATA_APPEND_KEYS,
    EXTRA_FORM_DATA_OVERRIDE_EXTRA_KEYS,
    EXTRA_FORM_DATA_OVERRIDE_KEYS,
    EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS,
    InstantTimeComparison,
    LRU_CACHE_MAX_SIZE,
    MODEL_API_RW_METHOD_PERMISSION_MAP,
    MODEL_VIEW_RW_METHOD_PERMISSION_MAP,
    NO_TIME_RANGE,
    NULL_STRING,
    PandasAxis,
    PandasPostprocessingCompare,
    PASSWORD_MASK,
    QUERY_CANCEL_KEY,
    QUERY_EARLY_CANCEL_KEY,
    RouteMethod,
    TimeGrain,
)


def test_null_string_constant() -> None:
    assert NULL_STRING == "<NULL>"


def test_empty_string_constant() -> None:
    assert EMPTY_STRING == "<empty string>"


def test_password_mask() -> None:
    assert PASSWORD_MASK == "X" * 10
    assert len(PASSWORD_MASK) == 10


def test_no_time_range() -> None:
    assert NO_TIME_RANGE == "No filter"


def test_query_cancel_keys() -> None:
    assert QUERY_CANCEL_KEY == "cancel_query"
    assert QUERY_EARLY_CANCEL_KEY == "early_cancel_query"


def test_lru_cache_max_size() -> None:
    assert LRU_CACHE_MAX_SIZE == 256


def test_examples_db_uuid_format() -> None:
    import uuid

    uuid.UUID(EXAMPLES_DB_UUID)


def test_change_me_secret_key() -> None:
    assert CHANGE_ME_SECRET_KEY == "CHANGE_ME_TO_A_COMPLEX_RANDOM_SECRET"  # noqa: S105


def test_instant_time_comparison_values() -> None:
    assert InstantTimeComparison.INHERITED == "r"
    assert InstantTimeComparison.YEAR == "y"
    assert InstantTimeComparison.MONTH == "m"
    assert InstantTimeComparison.WEEK == "w"


def test_instant_time_comparison_is_str_enum() -> None:
    assert isinstance(InstantTimeComparison.INHERITED, str)


def test_route_method_model_view_methods() -> None:
    assert RouteMethod.ADD == "add"
    assert RouteMethod.DELETE == "delete"
    assert RouteMethod.EDIT == "edit"
    assert RouteMethod.LIST == "list"
    assert RouteMethod.SHOW == "show"


def test_route_method_rest_model_view_methods() -> None:
    assert RouteMethod.EXPORT == "export"
    assert RouteMethod.IMPORT == "import_"
    assert RouteMethod.GET == "get"
    assert RouteMethod.GET_LIST == "get_list"
    assert RouteMethod.POST == "post"
    assert RouteMethod.PUT == "put"
    assert RouteMethod.RELATED == "related"
    assert RouteMethod.DISTINCT == "distinct"


def test_route_method_api_set() -> None:
    expected = {
        RouteMethod.API_CREATE,
        RouteMethod.API_DELETE,
        RouteMethod.API_GET,
        RouteMethod.API_READ,
        RouteMethod.API_UPDATE,
    }
    assert RouteMethod.API_SET == expected


def test_route_method_crud_set() -> None:
    assert RouteMethod.ADD in RouteMethod.CRUD_SET
    assert RouteMethod.LIST in RouteMethod.CRUD_SET
    assert RouteMethod.EDIT in RouteMethod.CRUD_SET
    assert RouteMethod.DELETE in RouteMethod.CRUD_SET


def test_route_method_rest_model_view_crud_set() -> None:
    assert RouteMethod.DELETE in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.GET in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.GET_LIST in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.POST in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.PUT in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.INFO in RouteMethod.REST_MODEL_VIEW_CRUD_SET


def test_model_view_rw_method_permission_map_read_ops() -> None:
    read_ops = ["api", "api_get", "api_read", "list", "show", "download"]
    for op in read_ops:
        assert MODEL_VIEW_RW_METHOD_PERMISSION_MAP[op] == "read"


def test_model_view_rw_method_permission_map_write_ops() -> None:
    write_ops = ["add", "api_create", "api_delete", "api_update", "delete", "edit"]
    for op in write_ops:
        assert MODEL_VIEW_RW_METHOD_PERMISSION_MAP[op] == "write"


def test_model_api_rw_method_permission_map_read_ops() -> None:
    read_ops = ["get", "get_list", "info", "distinct", "related"]
    for op in read_ops:
        assert MODEL_API_RW_METHOD_PERMISSION_MAP[op] == "read"


def test_model_api_rw_method_permission_map_write_ops() -> None:
    write_ops = ["post", "put", "delete", "bulk_delete", "import_"]
    for op in write_ops:
        assert MODEL_API_RW_METHOD_PERMISSION_MAP[op] == "write"


def test_extra_form_data_append_keys() -> None:
    assert "adhoc_filters" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "filters" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "interactive_groupby" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "interactive_highlight" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "interactive_drilldown" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "custom_form_data" in EXTRA_FORM_DATA_APPEND_KEYS


def test_extra_form_data_override_regular_mappings() -> None:
    assert (
        EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS["granularity_sqla"] == "granularity"
    )
    assert EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS["time_range"] == "time_range"


def test_extra_form_data_override_keys_combines_sources() -> None:
    regular_values = set(EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS.values())
    combined = regular_values | EXTRA_FORM_DATA_OVERRIDE_EXTRA_KEYS
    assert EXTRA_FORM_DATA_OVERRIDE_KEYS == combined


def test_time_grain_values() -> None:
    assert TimeGrain.SECOND == "PT1S"
    assert TimeGrain.MINUTE == "PT1M"
    assert TimeGrain.HOUR == "PT1H"
    assert TimeGrain.DAY == "P1D"
    assert TimeGrain.WEEK == "P1W"
    assert TimeGrain.MONTH == "P1M"
    assert TimeGrain.QUARTER == "P3M"
    assert TimeGrain.YEAR == "P1Y"


def test_time_grain_is_str_enum() -> None:
    assert isinstance(TimeGrain.DAY, str)
    assert f"grain={TimeGrain.DAY}" == "grain=P1D"


def test_pandas_axis_values() -> None:
    assert PandasAxis.ROW == 0
    assert PandasAxis.COLUMN == 1


def test_pandas_axis_is_int() -> None:
    assert isinstance(PandasAxis.ROW, int)
    assert isinstance(PandasAxis.COLUMN, int)


def test_pandas_postprocessing_compare_values() -> None:
    assert PandasPostprocessingCompare.DIFF == "difference"
    assert PandasPostprocessingCompare.PCT == "percentage"


def test_pandas_postprocessing_compare_is_str_enum() -> None:
    assert isinstance(PandasPostprocessingCompare.DIFF, str)
