""" Item pipelines for processing """

from itemadapter import ItemAdapter


class BookPipeline:
    """Normalize scraped book data before exporting or storing it."""

    def process_item(self, item, spider):
        """ Clean text fields, price, and availability """
        
        adapter = ItemAdapter(item)

        # normalize whitespace in text fields
        text_fields = ("title", "product_url", "image_url", "category")

        for field in text_fields:
            value = adapter.get(field)

            if value is not None:
                adapter[field] = " ".join(value.split())

        # convert price to number
        price = adapter.get("price")

        if price is not None:
            normalized_price = price.replace("£", "").strip()
            adapter["price"] = float(normalized_price)

        # convert availability to Boolean.
        availability = adapter.get("availability", "")
        adapter["availability"] = (" ".join(availability.split()) == "In stock")

        return item
