import pytest
from unittest.mock import patch, MagicMock
from cassandra_cli.executor import NodetoolExecutor


@pytest.fixture
def executor(monkeypatch):
    monkeypatch.setenv("NODETOOL_USER", "test_user")
    monkeypatch.setenv("NODETOOL_PASSWORD", "test_password")
    return NodetoolExecutor("test-ns", "test-pod")


def test_build_command(executor):
    command = executor.build_command(["status"])
    expected = [
        "kubectl",
        "exec",
        "-n",
        "test-ns",
        "test-pod",
        "-c",
        "cassandra",
        "--",
        "nodetool",
        "-Dcom.sun.jndi.rmiURLParsing=legacy",
        "-u",
        "test_user",
        "-pw",
        "test_password",
        "status",
    ]
    assert command == expected


@patch("subprocess.run")
def test_run_success(mock_run, executor):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "OK"
    mock_run.return_value = mock_result

    output = executor.run(["status"])
    assert output == "OK"
    mock_run.assert_called_once_with(
        executor.build_command(["status"]),
        capture_output=True,
        text=True,
    )


@patch("subprocess.run")
def test_run_error(mock_run, executor):
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Error"
    mock_run.return_value = mock_result

    with pytest.raises(RuntimeError, match="Error"):
        executor.run(["status"])
