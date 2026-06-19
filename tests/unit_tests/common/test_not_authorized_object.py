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

from superset.common.not_authorized_object import (
    NotAuthorizedException,
    NotAuthorizedObject,
)
from superset.exceptions import SupersetException


def test_not_authorized_object_getattr_raises() -> None:
    obj = NotAuthorizedObject("access the dashboard")
    with pytest.raises(NotAuthorizedException, match="access the dashboard"):
        _ = obj.some_attribute


def test_not_authorized_object_getitem_raises() -> None:
    obj = NotAuthorizedObject("view the chart")
    with pytest.raises(NotAuthorizedException, match="view the chart"):
        _ = obj["some_key"]


def test_not_authorized_object_different_attribute_raises() -> None:
    obj = NotAuthorizedObject("execute queries")
    with pytest.raises(NotAuthorizedException, match="execute queries"):
        _ = obj.another_attr


def test_not_authorized_exception_message() -> None:
    exc = NotAuthorizedException("view datasets")
    assert str(exc) == "The user is not authorized to view datasets"


def test_not_authorized_exception_default_message() -> None:
    exc = NotAuthorizedException()
    assert str(exc) == "The user is not authorized to "


def test_not_authorized_exception_is_superset_exception() -> None:
    exc = NotAuthorizedException("do something")
    assert isinstance(exc, SupersetException)


def test_not_authorized_exception_with_wrapped_exception() -> None:
    original = ValueError("original error")
    exc = NotAuthorizedException("perform action", exception=original)
    assert str(exc) == "The user is not authorized to perform action"
