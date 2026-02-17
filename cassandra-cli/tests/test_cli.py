import pytest
from unittest.mock import patch
from cassandra_cli.cli import parse_args, main
import sys


def test_parse_args_success():
    with patch.object(
        sys, "argv", ["cli.py", "--namespace", "test-ns", "--pod", "test-pod", "status"]
    ):
        namespace, pod, nodetool_args = parse_args()
        assert namespace == "test-ns"
        assert pod == "test-pod"
        assert nodetool_args == ["status"]


def test_parse_args_default_values():
    with patch.object(sys, "argv", ["cli.py", "status"]):
        namespace, pod, nodetool_args = parse_args()
        assert namespace == "cassandra"
        assert pod == "a-cassandra-0"
        assert nodetool_args == ["status"]


def test_parse_args_no_command():
    with (
        patch.object(sys, "argv", ["cli.py", "--namespace", "test-ns"]),
        pytest.raises(SystemExit),
    ):
        parse_args()


@patch("cassandra_cli.cli.NodetoolExecutor")
@patch("cassandra_cli.cli.logging.info")
def test_main_success(mock_logging_info, mock_executor):
    instance = mock_executor.return_value
    instance.run.return_value = "OK"
    with patch.object(sys, "argv", ["cli.py", "status"]):
        main()
        mock_logging_info.assert_called_with("OK")


@patch("cassandra_cli.cli.NodetoolExecutor")
@patch("cassandra_cli.cli.logging.info")
def test_main_error(mock_logging_info, mock_executor):
    instance = mock_executor.return_value
    instance.run.side_effect = RuntimeError("Error")
    with (
        patch.object(sys, "argv", ["cli.py", "status"]),
        pytest.raises(SystemExit) as e,
    ):
        main()
        mock_logging_info.assert_called_with("Error: Error")
        assert e.value.code == 1
