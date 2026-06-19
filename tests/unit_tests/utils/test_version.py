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

import subprocess
from unittest.mock import patch

from superset.utils.version import _get_local_branch, _get_local_sha, get_dev_env_label


def test_get_local_branch_returns_branch_name() -> None:
    with patch(
        "superset.utils.version.subprocess.check_output",
        return_value=b"my-feature-branch\n",
    ):
        assert _get_local_branch() == "my-feature-branch"


def test_get_local_branch_returns_none_for_detached_head() -> None:
    with patch(
        "superset.utils.version.subprocess.check_output",
        return_value=b"HEAD\n",
    ):
        assert _get_local_branch() is None


def test_get_local_branch_returns_none_on_error() -> None:
    with patch(
        "superset.utils.version.subprocess.check_output",
        side_effect=subprocess.CalledProcessError(128, "git"),
    ):
        assert _get_local_branch() is None


def test_get_local_branch_returns_none_on_timeout() -> None:
    with patch(
        "superset.utils.version.subprocess.check_output",
        side_effect=subprocess.TimeoutExpired(cmd="git", timeout=5),
    ):
        assert _get_local_branch() is None


def test_get_local_sha_returns_sha() -> None:
    with patch(
        "superset.utils.version.subprocess.check_output",
        return_value=b"abc123def456\n",
    ):
        assert _get_local_sha() == "abc123def456"


def test_get_local_sha_returns_none_on_error() -> None:
    with patch(
        "superset.utils.version.subprocess.check_output",
        side_effect=subprocess.CalledProcessError(128, "git"),
    ):
        assert _get_local_sha() is None


def test_get_dev_env_label_branch_and_sha() -> None:
    with (
        patch.dict(
            "os.environ",
            {"GITHUB_HEAD_REF": "feature-x", "GITHUB_SHA": "abc123def456ghij"},
            clear=False,
        ),
        patch("superset.utils.version._get_local_branch", return_value=None),
        patch("superset.utils.version._get_local_sha", return_value=None),
    ):
        result = get_dev_env_label()
        assert result == "feature-x@abc123de"


def test_get_dev_env_label_sha_only() -> None:
    with (
        patch.dict(
            "os.environ",
            {"GITHUB_SHA": "abc123def456ghij"},
            clear=False,
        ),
        patch.dict("os.environ", {}, clear=False),
        patch("superset.utils.version._get_local_branch", return_value=None),
        patch("superset.utils.version._get_local_sha", return_value=None),
    ):
        # Remove GITHUB_HEAD_REF and GITHUB_REF_NAME if they exist
        import os

        os.environ.pop("GITHUB_HEAD_REF", None)
        os.environ.pop("GITHUB_REF_NAME", None)
        result = get_dev_env_label()
        assert result == "@abc123de"


def test_get_dev_env_label_branch_only() -> None:
    import os

    with (
        patch.dict(
            "os.environ",
            {"GITHUB_HEAD_REF": "main"},
            clear=False,
        ),
        patch("superset.utils.version._get_local_branch", return_value=None),
        patch("superset.utils.version._get_local_sha", return_value=None),
    ):
        os.environ.pop("GITHUB_SHA", None)
        result = get_dev_env_label()
        assert result == "main"


def test_get_dev_env_label_empty() -> None:
    import os

    with (
        patch("superset.utils.version._get_local_branch", return_value=None),
        patch("superset.utils.version._get_local_sha", return_value=None),
    ):
        os.environ.pop("GITHUB_HEAD_REF", None)
        os.environ.pop("GITHUB_REF_NAME", None)
        os.environ.pop("GITHUB_SHA", None)
        result = get_dev_env_label()
        assert result == ""


def test_get_dev_env_label_falls_back_to_local_git() -> None:
    import os

    with (
        patch("superset.utils.version._get_local_branch", return_value="local-branch"),
        patch("superset.utils.version._get_local_sha", return_value="localsha123456"),
    ):
        os.environ.pop("GITHUB_HEAD_REF", None)
        os.environ.pop("GITHUB_REF_NAME", None)
        os.environ.pop("GITHUB_SHA", None)
        result = get_dev_env_label()
        assert result == "local-branch@localsha"
