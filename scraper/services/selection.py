""" Randomly selecting categories and books """

import random

def select_categories(categories):
    """Select five random books."""
    return random.sample(categories, 5)


def select_books(books):
    """Select five random books."""
    return random.sample(books, min(5, len(books)))
