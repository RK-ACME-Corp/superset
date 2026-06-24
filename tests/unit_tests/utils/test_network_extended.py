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

import socket
from unittest.mock import MagicMock, patch

from superset.utils.network import is_host_up, is_hostname_valid, is_port_open


def test_is_port_open_success() -> None:
    mock_socket = MagicMock()
    with (
        patch("superset.utils.network.socket.getaddrinfo") as mock_getaddrinfo,
        patch("superset.utils.network.socket.socket", return_value=mock_socket),
    ):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.1", 80))
        ]
        assert is_port_open("localhost", 80) is True
        mock_socket.settimeout.assert_called_once_with(5)
        mock_socket.connect.assert_called_once_with(("127.0.0.1", 80))
        mock_socket.shutdown.assert_called_once_with(socket.SHUT_RDWR)
        mock_socket.close.assert_called_once()


def test_is_port_open_connection_refused() -> None:
    mock_socket = MagicMock()
    mock_socket.connect.side_effect = OSError("Connection refused")
    with (
        patch("superset.utils.network.socket.getaddrinfo") as mock_getaddrinfo,
        patch("superset.utils.network.socket.socket", return_value=mock_socket),
    ):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("127.0.0.1", 9999))
        ]
        assert is_port_open("localhost", 9999) is False
        mock_socket.close.assert_called_once()


def test_is_port_open_multiple_addresses_first_fails() -> None:
    mock_socket_fail = MagicMock()
    mock_socket_fail.connect.side_effect = OSError("Connection refused")
    mock_socket_ok = MagicMock()
    sockets = [mock_socket_fail, mock_socket_ok]
    with (
        patch("superset.utils.network.socket.getaddrinfo") as mock_getaddrinfo,
        patch("superset.utils.network.socket.socket", side_effect=sockets),
    ):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("10.0.0.1", 80)),
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("10.0.0.2", 80)),
        ]
        assert is_port_open("multi-host", 80) is True


def test_is_hostname_valid_resolvable() -> None:
    with patch("superset.utils.network.socket.getaddrinfo") as mock_getaddrinfo:
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 0))
        ]
        assert is_hostname_valid("example.com") is True


def test_is_hostname_valid_unresolvable() -> None:
    with patch(
        "superset.utils.network.socket.getaddrinfo",
        side_effect=socket.gaierror("Name or service not known"),
    ):
        assert is_hostname_valid("nonexistent.invalid") is False


def test_is_host_up_success() -> None:
    with patch("superset.utils.network.subprocess.call", return_value=0) as mock_call:
        assert is_host_up("example.com") is True
        mock_call.assert_called_once()
        args = mock_call.call_args[0][0]
        assert "ping" in args
        assert "example.com" in args


def test_is_host_up_failure() -> None:
    with patch("superset.utils.network.subprocess.call", return_value=1):
        assert is_host_up("unreachable.invalid") is False


def test_is_host_up_timeout() -> None:
    import subprocess

    with patch(
        "superset.utils.network.subprocess.call",
        side_effect=subprocess.TimeoutExpired(cmd="ping", timeout=5),
    ):
        assert is_host_up("slow-host.invalid") is False
