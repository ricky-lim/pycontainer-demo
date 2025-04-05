import pytest
from typer.testing import CliRunner
from robot.cli import app
from robot.robot_repository import RobotRepository

runner = CliRunner()


@pytest.fixture
def sqlite_db():
    repo = RobotRepository("sqlite:///:memory:")
    repo.init_db()
    return repo


@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, sqlite_db):
    def mock_get_db(_):
        return sqlite_db

    monkeypatch.setattr("robot.cli.get_db", mock_get_db)


@pytest.mark.unit
def test_cli_shows_help_by_default():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Usage: " in result.stdout


@pytest.mark.unit
def test_add_robot():
    result = runner.invoke(app, ["add", "-n", "R2D2", "-d", "Astromech droid"])
    assert result.exit_code == 0
    assert "Robot created successfully" in result.stdout


@pytest.mark.unit
def test_get_robot_by_id(sqlite_db):
    robot_id = sqlite_db.add_robot("R2D2", "Astromech droid")
    result = runner.invoke(app, ["get", "--id", str(robot_id)])
    assert result.exit_code == 0
    assert "R2D2" in result.stdout
    assert "Astromech droid" in result.stdout


@pytest.mark.unit
def test_get_robot_by_name(sqlite_db):
    sqlite_db.add_robot("R2D2", "Astromech droid")
    result = runner.invoke(app, ["get", "--name", "R2D2"])
    assert result.exit_code == 0
    assert "R2D2" in result.stdout
    assert "Astromech droid" in result.stdout


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
