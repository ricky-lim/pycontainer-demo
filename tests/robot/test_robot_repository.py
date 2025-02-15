import pytest


@pytest.mark.integration
def test_add_robot(robot_repository):
    robot_id = robot_repository.add_robot("pixie", "cleaning up my garden")
    assert robot_id == 1


@pytest.mark.integration
def test_get_robot_by_name(robot_repository):
    robot_repository.add_robot("XOXO", "A Rolling droid")
    robot = robot_repository.get_robot_by_name("XOXO")
    assert robot.name == "XOXO"


@pytest.mark.integration
def test_get_robot_by_id(robot_repository):
    robot_id = robot_repository.add_robot("HOHO", "A laughing pod")
    robot = robot_repository.get_robot_by_id(robot_id)
    assert robot.name == "HOHO"
    assert robot.description == "A laughing pod"
