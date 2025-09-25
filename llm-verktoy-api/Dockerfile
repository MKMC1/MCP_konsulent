FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY ./pyproject.toml .
RUN uv sync
ENV PATH="/app/.venv/bin:$PATH"

COPY /app app/
COPY /tests tests/

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
