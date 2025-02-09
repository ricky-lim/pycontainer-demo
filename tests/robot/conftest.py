import pytest
import docker
from testcontainers.postgres import PostgresContainer
from robot.robot_repository import RobotRepository

POSTGRES_IMAGE = "postgres:17-alpine"
DOCKER_HOST = "host.docker.internal"


@pytest.fixture(scope="session")
def docker_client():
    return docker.from_env()


@pytest.fixture(scope="session")
def robot_docker_image(docker_client, request):
    dockerfile = request.config.rootpath / "Dockerfile"
    image, _ = docker_client.images.build(
        path=str(dockerfile.parent),
        dockerfile=dockerfile.name,
        tag="robot:test",
    )

    request.addfinalizer(lambda: docker_client.images.remove(image.id, force=True))
    return image


@pytest.fixture(scope="function")
def postgres_container():
    with PostgresContainer(POSTGRES_IMAGE) as postgres:
        yield postgres


@pytest.fixture
def robot_repository(postgres_container):
    repo = RobotRepository(postgres_container.get_connection_url())
    repo.init_db()
    return repo


@pytest.fixture(scope="function")
def docker_robot(postgres_container, robot_docker_image, docker_client):
    def _run_robot_command(command: list[str]):
        return docker_client.containers.run(
            robot_docker_image.id,
            command=command,
            tty=True,
            stderr=True,
            stdout=True,
            extra_hosts={DOCKER_HOST: "host-gateway"},
            environment={
                "PGUSER": postgres_container.username,
                "PGPASSWORD": postgres_container.password,
                "PGHOST": DOCKER_HOST,
                "PGPORT": postgres_container.get_exposed_port(5432),
                "PGDATABASE": postgres_container.dbname,
            },
        )

    return _run_robot_command
