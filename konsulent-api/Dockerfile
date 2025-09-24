FROM python:3.14
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY ./pyproject.toml .
RUN uv sync --frozen --system

# Kopier kun denne tjenestens kode
COPY ./konsulent-api/app app/
COPY ./konsulent-api/tests tests/

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
