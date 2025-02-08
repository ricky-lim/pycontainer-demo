FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY src src/
COPY README.md .
COPY uv.lock .

# Create and use virtual environment
RUN uv venv .venv
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync 

ENTRYPOINT ["robot"]
