# Enterprise Web Scraping Pipeline

A Scrapy-based pipeline that scrapes book data from [Books to Scrape](https://books.toscrape.com/), processes it, and exports it to JSON, CSV, XML, and SQLite.

## Features

- Dynamically discovers book categories.
- Randomly selects up to five categories and up to five books per category.
- Handles category pagination.
- Extracts titles, prices, availability, product URLs, image URLs, and categories.
- Normalizes text, converts prices to numeric values, and availability to Boolean values.
- Exports processed items to JSON, CSV, and XML.
- Stores items in SQLite.
- Supports Docker execution and Scrapyd deployment.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker (optional, for containerized execution)

## Setup

```bash
git clone https://github.com/tanvir-005/Enterprise-Web-Scraping-Pipeline.git
cd Enterprise-Web-Scraping-Pipeline
uv sync --frozen
```

## Run locally

```bash
uv run scrapy crawl books
```

Generated files are written to the project directory:

- `books.json`
- `books.csv`
- `books.xml`
- `books.db`

Each crawl replaces the existing SQLite records.

## Docker

Build the image:

```bash
docker build -t books-scraper .
```

Run the spider:

```bash
docker run --rm books-scraper
```

Outputs are created inside the container at `/app`. With `--rm` and no volume mount, they are not retained on the host.

## Scrapyd

Start the server:

```bash
uv run scrapyd
```

In another terminal, deploy the project:

```bash
uv run scrapyd-deploy
```

Check the deployed spiders:

```bash
curl "http://127.0.0.1:6800/listspiders.json?project=scraper"
```

Schedule a crawl:

```bash
curl http://127.0.0.1:6800/schedule.json \
  -d project=scraper \
  -d spider=books
```

Check job status:

```bash
curl "http://127.0.0.1:6800/listjobs.json?project=scraper"
```

## Configuration

- `scraper/settings.py`: feed exports and pipeline configuration.
- `scraper/selectors.py`: CSS selectors.
- `scraper/services/selection.py`: random selection logic.
- `scraper/pipelines.py`: data normalization and SQLite storage.
- `scrapy.cfg` and `scrapyd.conf`: project and Scrapyd configuration.
- `Dockerfile`: container image configuration.
