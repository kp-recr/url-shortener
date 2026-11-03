FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY url-shortener-api/pyproject.toml url-shortener-api/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project \
    --python /usr/local/bin/python

COPY url-shortener-api/ ./

ENV PATH="/app/.venv/bin:$PATH" \
    UV_PYTHON_DOWNLOADS=never

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
