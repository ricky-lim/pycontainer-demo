# pycontainer-demo

![CI Status](https://github.com/ricky-lim/pycontainer-demo/actions/workflows/ci.yml/badge.svg)
[![Changelog](https://img.shields.io/badge/changelog-Common%20Changelog-blue.svg)](CHANGELOG.md)

A demonstration project showing how to effectively test dockerized Python applications using docker ❤️ testcontainers ❤️ pytest.

This project serves as a practical guide for implementing container-based testing strategies with automated CI pipelines.

It's only Continuous Integration (CI), not Continuous Deployment (CD), as this is a demo and not intended to publish artifacts to PyPI or Docker Hub.

## Features

- Docker containerization of Python applications
- Integration testing with TestContainers
- Pytest-based test suite
- Example of testing database interactions
- Automated CI with GitHub Actions

## Prerequisites

- Docker installed and running
- Python 3.12+
- uv package manager

## Installation

First, install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then clone and set up the project:

```bash
git clone https://github.com/ricky-lim/pycontainer-demo.git
cd pycontainer-demo

# Setup virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev,test]"
```

Running tests

```bash
pytest
```

Project Structure

```
├── src/               # Application source code
├── tests/             # Test files
├── .github/workflows/ # GitHub Actions workflows
├── pyproject.toml     # Project configuration
└── Dockerfile         # Dockerfile for building the app
```

Install pre-commit hooks

```bash
pre-commit install
```

Apply branch protection rules

```bash
gh api --method PUT /repos/ricky-lim/pycontainer-demo/branches/main/protection \
  --input branch-protection-rules.json
```

## Usage

For a demo, there is an app "robot".

To run it:

- Ensure you have postgress running

```bash
# Start PostgreSQL container
$ docker run -d --name robot-postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=postgres \
    -p 5432:5432 \
    postgres:17-alpine

# Wait for PostgreSQL to be ready
$ until docker exec robot-postgres pg_isready -U postgres; do echo "Waiting for PostgreSQL..."; sleep 1; done
```

- Run the app

```bash
# Build the app
$ docker build -t robot .
$ docker run -it --network host robot add --name pixie --description "cleaning up my garden"
```

- Check the database

```bash
# Check if the robot was added
$ docker exec -it robot-postgres psql -U postgres -d postgres -c "SELECT * FROM robot;"

 id | name  |      description
----+-------+-----------------------
  1 | pixie | cleaning up my garden
(1 row)
```

## CI Pipeline

The project includes a GitHub Actions workflow for CI. The workflow runs tests on every push to the main branch and on pull requests.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-new-feature`)
5. Open a pull request

## License

This project is licensed under Apache 2.0
