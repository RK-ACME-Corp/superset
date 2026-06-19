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


from superset.utils.urls import is_secure_url, modify_url_query


def test_is_secure_url_https() -> None:
    assert is_secure_url("https://example.com") is True


def test_is_secure_url_http() -> None:
    assert is_secure_url("http://example.com") is False


def test_is_secure_url_https_with_path() -> None:
    assert is_secure_url("https://example.com/path/to/page") is True


def test_is_secure_url_http_with_port() -> None:
    assert is_secure_url("http://example.com:8080/page") is False


def test_is_secure_url_empty_string() -> None:
    assert is_secure_url("") is False


def test_is_secure_url_no_scheme() -> None:
    assert is_secure_url("example.com") is False


def test_is_secure_url_ftp() -> None:
    assert is_secure_url("ftp://example.com") is False


def test_modify_url_query_add_new_param() -> None:
    url = "http://example.com/page"
    result = modify_url_query(url, key="value")
    assert "key=value" in result


def test_modify_url_query_replace_existing_param() -> None:
    url = "http://example.com/page?standalone=true"
    result = modify_url_query(url, standalone="false")
    assert "standalone=false" in result
    assert "standalone=true" not in result


def test_modify_url_query_multiple_params() -> None:
    url = "http://example.com/page"
    result = modify_url_query(url, a="1", b="2")
    assert "a=1" in result
    assert "b=2" in result


def test_modify_url_query_preserves_path() -> None:
    url = "http://example.com/my/path"
    result = modify_url_query(url, key="val")
    assert "/my/path" in result


def test_modify_url_query_with_list_value() -> None:
    url = "http://example.com/page"
    result = modify_url_query(url, items=["a", "b"])
    assert "items=" in result
