from datetime import date

from django.utils.text import slugify

from catalog.models import Book

data = [
    ('Rich Dad Poor Dad', 1997, 336, 250, 'paper', True),
    ('Fluent Python', 2022, 1012, 650, 'paper', True),
    ('Python Crash Course', 2019, 544, 420, 'ebook', True),
    ('Automate the Boring Stuff with python', 2015, 504, 380, 'paper', False),
    ('Learning PYTHON', 2013, 1648, 700, 'paper', True),
    ('Effective Python', 2020, 480, 390, 'ebook', True),
    ('Python Tricks', 2017, 302, 270, 'ebook', True),
    ('Two Scoops of Django', 2020, 532, 510, 'ebook', False),
    ('Clean Code', 2008, 464, 450, 'paper', True),
    ('The Pragmatic Programmer', 2019, 352, 480, 'audio', True),
    ('Refactoring', 2018, 448, 530, 'paper', False),
    ('Design Patterns', 1994, 395, 600, 'paper', True),
    ('Grokking Algorithms', 2016, 256, 300, 'ebook', True),
    ('Code Complete', 2004, 960, 550, 'paper', False),
    ('Designing Data-Intensive Applications', 2017, 616, 620, 'paper', True),
    ('The Clean Coder', 2011, 256, 250, 'audio', True),
    ('Atomic Habits', 2018, 320, 299, 'audio', True),
    ('Sapiens', 2014, 498, 350, 'paper', True),
    ('The Mythical Man-Month', 1995, 336, 200, 'audio', False),
    ('Deep Work', 2021, 296, 280, 'ebook', True),
]

books = []

for i, (title, year, pages, price, fmt, available) in enumerate(data, start=1):
    books.append(Book(
        title=title,
        slug=slugify(title),
        isbn=f'978{i:010d}',
        published_year=date(year, 1, 1),
        pages=pages,
        price=price,
        format=fmt,
        is_available=available,
    ))

Book.objects.bulk_create(books)

print(Book.objects.count())
