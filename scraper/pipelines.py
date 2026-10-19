
"""Item pipelines for processing and storing scraped books."""

import sqlite3
from pathlib import Path

from itemadapter import ItemAdapter


class BookPipeline:
    """Normalize scraped book data."""

    def process_item(self, item, spider):
        """Clean text fields, price, and availability."""
        adapter = ItemAdapter(item)

        text_fields = (
            "title",
            "product_url",
            "image_url",
            "category",
        )

        for field in text_fields:
            value = adapter.get(field)

            if value is not None:
                adapter[field] = " ".join(value.split())

        price = adapter.get("price")

        if price is not None:
            adapter["price"] = float(
                price.replace("£", "").strip()
            )

        availability = adapter.get("availability", "")
        adapter["availability"] = (
            " ".join(availability.split()) == "In stock"
        )

        return item


class SQLitePipeline:
    """Store normalized book items in SQLite."""

    def open_spider(self, spider):
        """Open the database and prepare the books table."""
        database_path = Path(__file__).resolve().parent.parent / "books.db"

        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                availability BOOLEAN NOT NULL,
                product_url TEXT NOT NULL,
                image_url TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)

        # Each crawl replaces the previous crawl's records.
        self.cursor.execute("DELETE FROM books")
        self.connection.commit()

        spider.logger.info(
            "SQLite database opened: %s",
            database_path,
        )

    def process_item(self, item, spider):
        """Insert a normalized book into the database."""
        adapter = ItemAdapter(item)

        self.cursor.execute("""
            INSERT INTO books (
                title,
                price,
                availability,
                product_url,
                image_url,
                category
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            adapter["title"],
            adapter["price"],
            adapter["availability"],
            adapter["product_url"],
            adapter["image_url"],
            adapter["category"],
        ))

        self.connection.commit()

        return item

    def close_spider(self, spider):
        """Close the database connection."""
        self.connection.close()

        spider.logger.info("SQLite database connection closed.")
