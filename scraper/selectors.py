""" Selectors to Scrape """

CATEGORY_LINKS = ".side_categories ul li ul li a[href]"

BOOK_CARDS = "article.product_pod"

NEXT_PAGE_LINK = "li.next a[href]"

CARD_TITLE = "h3 a[title]"
CARD_PRICE = "p.price_color"
CARD_AVAILABILITY = "p.availability"
CARD_PRODUCT_URL = "h3 a[href]"
CARD_IMAGE_URL = "div.image_container img[src]"