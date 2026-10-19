""" Spider for scraping """

import scrapy

from scraper import selectors
from scraper.items import BookItem
from scraper.services.selection import select_books as choose_books, select_categories as choose_categories


class BooksSpider(scrapy.Spider):
    """ Discover categories and scrape books """

    name = "books"
    start_urls = ["https://books.toscrape.com/index.html"]


    def parse(self, response):
        """ Discover categories and visit the selected categories """
        categories = self.identify_categories(response)
        selected_categories = self.select_categories(categories)

        yield from self.visit_categories(selected_categories)


    def identify_categories(self, response):
        """ Extract all category names and URLs """
        categories = []

        for link in response.css(selectors.CATEGORY_LINKS):
            name = " ".join(link.css("::text").getall()).strip()
            url = response.urljoin(link.attrib["href"])

            categories.append({"name": name, "url": url})

        self.logger.info("Identified %d categories.", len(categories))

        return categories


    def select_categories(self, categories):
        """ Select five categories """
        selected = choose_categories(categories)

        self.logger.info("Selected %d of %d available categories.", len(selected), len(categories))

        return selected


    def visit_categories(self, categories):
        """ Request each selected category """
        for category in categories:
            yield scrapy.Request(
                url=category["url"],
                callback=self.parse_category,
                cb_kwargs={
                    "category_name": category["name"],
                    "books": [],
                },
            )


    def parse_category(self, response, category_name, books):
        """ Collect books of a category """
        books.extend(
            self.identify_books(response, category_name)
        )

        next_page = response.css(selectors.NEXT_PAGE_LINK + "::attr(href)").get()

        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_category,
                cb_kwargs={
                    "category_name": category_name,
                    "books": books,
                },
            )
            return

        self.logger.info(
            "Category '%s': found %d distinct books.",
            category_name,
            len(books),
        )

        selected_books = self.select_books(books)

        for book in selected_books:
            self.logger.info("Selected book: %s | %s", book["title"], book["product_url"])
            yield BookItem(**book)


    def identify_books(self, response, category_name):
        """ Extract book data """
 
        books = []
        for card in response.css(selectors.BOOK_CARDS):
            book = self.parse_book_card(card, response, category_name)

            if book and all(book.values()):
                books.append(book)
            else:
                self.logger.warning("Skipping incomplete book card on %s.", response.url)

        return books


    def select_books(self, books):
        """ Select five books """
 
        selected = choose_books(books)
        self.logger.info("Selected %d of %d available books.", len(selected), len(books))

        return selected


    def parse_book_card(self, card, response, category_name):
        """ Extract the six fields """
        title = card.css(selectors.CARD_TITLE + "::attr(title)").get()
        price = card.css(selectors.CARD_PRICE + "::text").get()

        availability = " ".join(card.css(selectors.CARD_AVAILABILITY + " ::text").getall()).strip()
        product_path = card.css(selectors.CARD_PRODUCT_URL + "::attr(href)").get()
        image_path = card.css(selectors.CARD_IMAGE_URL + "::attr(src)").get()

        return {
            "title": title,
            "price": price,
            "availability": availability,
            "product_url": (response.urljoin(product_path)if product_path else None),
            "image_url": (response.urljoin(image_path)if image_path else None),
            "category": category_name,
        }