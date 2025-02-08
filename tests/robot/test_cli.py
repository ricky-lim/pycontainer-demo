import pytest
from robot.robot_repository import Robot
from typer.testing import CliRunner
from robot.cli import app
from unittest.mock import Mock, patch

runner = CliRunner()


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
def test_add_robot_with_mocked_db(mock_db):
    # Arrange
    mock_db.add_robot.return_value = 1

    # Act
    result = runner.invoke(app, ["add", "-n", "R2D2", "-d", "Astromech droid"])

    # Assert
    assert result.exit_code == 0
    mock_db.add_robot.assert_called_once_with("R2D2", "Astromech droid")


@pytest.mark.unit
def test_get_robot_with_mocked_db(mock_db):
    # Arrange
    mock_robot = Robot(id=1, name="R2D2", description="Astromech droid")
    mock_db.get_robot_by_id.return_value = mock_robot

    # Act
    result = runner.invoke(app, ["get", "--id", "1"])

    #  Assert
    assert result.exit_code == 0
    mock_db.get_robot_by_id.assert_called_once_with(1)


@pytest.mark.unit
def test_add_robot_requires_name_and_description():
    # Act
    result = runner.invoke(app, ["add"])

    # Assert
    assert result.exit_code == 2
    assert "Missing option" in result.stdout


@pytest.mark.unit
def test_find_robot_requires_name_or_id():
    # Act
    result = runner.invoke(app, ["get"])

    # Assert
    assert result.exit_code == 1
    assert "Please provide either a name or an ID." in result.stdout
