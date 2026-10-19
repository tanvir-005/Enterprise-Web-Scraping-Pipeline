
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock .python-version ./
COPY README.md ./
COPY scrapy.cfg ./
COPY scraper/ ./scraper/
COPY src/ ./src/

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "--frozen", "scrapy", "crawl", "books"]
