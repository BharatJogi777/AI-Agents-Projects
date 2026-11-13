FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
RUN groupadd --system app && useradd --system --gid app --home-dir /app app
COPY pyproject.toml README.md ./
COPY app ./app
RUN pip install --no-cache-dir .
USER app
ENTRYPOINT ["python", "-m", "app.server"]
