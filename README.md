# pycontainer-demo

![CI workflow](https://github.com/github/docs/actions/workflows/ci.yml/badge.svg)

Python containerization demo with PostgreSQL, testcontainers for integration testing, and GitHub Actions CI/CD.

For a demo, there is a app named "robot".

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

## Development

- Setup virtual environment `uv venv`
- Activate virtual environment `source .venv/bin/activate`
- Install dependencies `uv pip install -e ".[dev,test]"`
- Run test `pytest`
- Install precommit `pre-commit install`
