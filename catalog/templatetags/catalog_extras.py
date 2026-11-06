from math import ceil

from django import template

from catalog.models import Book

register = template.Library()

WORDS_PER_MINUTE = 120


@register.filter
def reading_time(text):
    if not text:
        return "-"

    word_count = len(text.split())

    if not word_count:
        return "-"

    result = ceil(word_count / WORDS_PER_MINUTE)
    return f"~ {result} {'minute' if result == 1 else 'minutes'} reading"


@register.inclusion_tag("partials/latest_books.html")
def latest_books(count):
    books = Book.objects.select_related("author").order_by("-created_at")[:count]
    return {"books": books}


@register.inclusion_tag("components/rating.html")
def rating(value, css_class=""):
    return {"filled": "★" * value, "off": "★" * (5 - value), "css_class": css_class}
