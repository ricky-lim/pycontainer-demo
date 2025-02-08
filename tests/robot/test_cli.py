import pytest
from robot.robot_repository import Robot
from typer.testing import CliRunner
from robot.cli import app
from unittest.mock import Mock, patch

runner = CliRunner()
TEST_ROBOT = Robot(id=1, name="R2D2", description="Astromech droid")


@pytest.fixture
def mock_db():
    with patch("robot.cli.get_db") as mock:
        mock_repo = Mock()
        mock.return_value = mock_repo
        yield mock_repo


@pytest.mark.unit
def test_cli_shows_help_by_default():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Robot Management System" in result.stdout


@pytest.mark.unit
@pytest.mark.parametrize(
    "command,args,expected_call",
    [
        (
            "add",
            ["-n", "R2D2", "-d", "Astromech droid"],
            ("add_robot", ("R2D2", "Astromech droid")),
        ),
        ("get", ["--id", "1"], ("get_robot_by_id", (1,))),
        ("get", ["--name", "R2D2"], ("get_robot_by_name", ("R2D2",))),
    ],
)
def test_robot_commands(mock_db, command, args, expected_call):
    method_name, method_args = expected_call
    getattr(mock_db, method_name).return_value = TEST_ROBOT

    result = runner.invoke(app, [command, *args])

    assert result.exit_code == 0
    getattr(mock_db, method_name).assert_called_once_with(*method_args)


@pytest.mark.unit
@pytest.mark.parametrize(
    "command,expected_message",
    [
        (["add"], "Missing option"),
        (["get"], "Please provide either a name or an ID."),
    ],
)
def test_command_validations(command, expected_message):
    result = runner.invoke(app, command)
    assert expected_message in result.stdout
    assert result.exit_code != 0
