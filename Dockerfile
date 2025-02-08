FROM python:3.12-slim

# # Install PostgreSQL development files
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY src src/

RUN pip install .

ENTRYPOINT ["robot"]
