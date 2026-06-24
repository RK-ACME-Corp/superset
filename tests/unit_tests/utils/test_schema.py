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

import pytest
from marshmallow import ValidationError

from superset.utils.schema import (
    OneOfCaseInsensitive,
    validate_external_url,
    validate_json,
)


def test_one_of_case_insensitive_valid_exact_match() -> None:
    validator = OneOfCaseInsensitive(choices=["foo", "bar", "baz"])
    assert validator("foo") == "foo"


def test_one_of_case_insensitive_valid_different_case() -> None:
    validator = OneOfCaseInsensitive(choices=["foo", "bar", "baz"])
    assert validator("FOO") == "FOO"
    assert validator("Bar") == "Bar"
    assert validator("BAZ") == "BAZ"


def test_one_of_case_insensitive_invalid() -> None:
    validator = OneOfCaseInsensitive(choices=["foo", "bar"])
    with pytest.raises(ValidationError):
        validator("qux")


def test_one_of_case_insensitive_non_string() -> None:
    validator = OneOfCaseInsensitive(choices=[1, 2, 3])
    assert validator(1) == 1


def test_one_of_case_insensitive_non_string_invalid() -> None:
    validator = OneOfCaseInsensitive(choices=[1, 2, 3])
    with pytest.raises(ValidationError):
        validator(4)


def test_validate_json_valid() -> None:
    validate_json('{"key": "value"}')


def test_validate_json_valid_array() -> None:
    validate_json("[1, 2, 3]")


def test_validate_json_invalid() -> None:
    with pytest.raises(ValidationError, match="JSON not valid"):
        validate_json("{invalid json}")


def test_validate_json_empty_object() -> None:
    validate_json("{}")


def test_validate_external_url_valid_https() -> None:
    validate_external_url("https://example.com/path")


def test_validate_external_url_valid_http() -> None:
    validate_external_url("http://example.com/path")


def test_validate_external_url_empty_string() -> None:
    validate_external_url("")


def test_validate_external_url_none() -> None:
    validate_external_url(None)


def test_validate_external_url_javascript_scheme() -> None:
    with pytest.raises(ValidationError, match="URL must use one of the following"):
        validate_external_url("javascript:alert(1)")


def test_validate_external_url_data_scheme() -> None:
    with pytest.raises(ValidationError, match="URL must use one of the following"):
        validate_external_url("data:text/html,<script>alert(1)</script>")


def test_validate_external_url_ftp_scheme() -> None:
    with pytest.raises(ValidationError, match="URL must use one of the following"):
        validate_external_url("ftp://example.com/file")


def test_validate_external_url_no_host() -> None:
    with pytest.raises(ValidationError, match="URL must be absolute"):
        validate_external_url("https:")
