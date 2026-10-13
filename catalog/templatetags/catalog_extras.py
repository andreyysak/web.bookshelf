from math import ceil
from django import template
from catalog.data import BOOKS

register = template.Library()

WORDS_PER_MINUTE = 120


@register.filter
def reading_time(text):
    if not text:
        return '-'

    word_count = len(text.split())

    if not word_count:
        return '-'

    result = ceil(word_count / WORDS_PER_MINUTE)
    return f'~ {result} {'minute' if result == 1 else 'minutes'} reading'


@register.inclusion_tag('includes/latest_books.html')
def latest_books(count):
    books = sorted(BOOKS, key=lambda book: book['published'], reverse=True)[:count]
    return {'books': books}
