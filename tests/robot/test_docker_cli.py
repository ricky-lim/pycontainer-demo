import pytest


@pytest.mark.end_to_end
def test_robot_add_and_get(docker_robot):
    # Create robot
    result = docker_robot(
        [
            "add",
            "--name",
            "pixie",
            "--description",
            "cleaning up my garden",
        ]
    )
    assert "Robot created successfully" in result.decode()

    # Verify using both name and id lookups
    for get_cmd in [
        ["get", "--name", "pixie"],
        ["get", "--id", "1"],
    ]:
        result = docker_robot(get_cmd)
        output = result.decode()
        assert "pixie" in output
        assert "cleaning up my garden" in output
