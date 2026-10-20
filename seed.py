from datetime import date

from django.utils.text import slugify

from catalog.models import Book, Author, AuthorProfile, Genre, BookGenre

# name: (birth_date, website)
authors_data = {
    'Robert Kiyosaki': (date(1947, 4, 8), 'https://www.richdad.com'),
    'Luciano Ramalho': (None, 'https://www.fluentpython.com'),
    'Eric Matthes': (None, ''),
    'Al Sweigart': (None, 'https://inventwithpython.com'),
    'Mark Lutz': (None, ''),
    'Brett Slatkin': (None, ''),
    'Dan Bader': (None, 'https://dbader.org'),
    'Daniel Roy Greenfeld': (None, ''),
    'Robert C. Martin': (date(1952, 12, 5), 'http://cleancoder.com'),
    'David Thomas': (None, ''),
    'Martin Fowler': (date(1963, 12, 18), 'https://martinfowler.com'),
    'Erich Gamma': (date(1961, 3, 13), ''),
    'Aditya Bhargava': (None, ''),
    'Steve McConnell': (None, ''),
    'Martin Kleppmann': (None, 'https://martin.kleppmann.com'),
    'James Clear': (date(1986, 1, 22), 'https://jamesclear.com'),
    'Yuval Noah Harari': (date(1976, 2, 24), 'https://www.ynharari.com'),
    'Fred Brooks': (date(1931, 4, 19), ''),
    'Cal Newport': (date(1982, 6, 23), 'https://calnewport.com'),
    'Terry Pratchett': (date(1948, 4, 28), 'https://www.terrypratchett.co.uk'),
    'J.R.R. Tolkien': (date(1892, 1, 3), ''),
}

genres_data = [
    'Programming', 'Python', 'Django', 'Software Engineering', 'Algorithms',
    'Self-help', 'Finance', 'History', 'Fantasy',
]

# (title, year, pages, price, format, available, author, genres)
books_data = [
    ('Rich Dad Poor Dad', 1997, 336, 250, 'paper', True, 'Robert Kiyosaki', ['Finance', 'Self-help']),
    ('Fluent Python', 2022, 1012, 650, 'paper', True, 'Luciano Ramalho', ['Programming', 'Python']),
    ('Python Crash Course', 2019, 544, 420, 'ebook', True, 'Eric Matthes', ['Programming', 'Python']),
    ('Automate the Boring Stuff with python', 2015, 504, 380, 'paper', False, 'Al Sweigart', ['Programming', 'Python']),
    ('Learning PYTHON', 2013, 1648, 700, 'paper', True, 'Mark Lutz', ['Programming', 'Python']),
    ('Effective Python', 2020, 480, 390, 'ebook', True, 'Brett Slatkin', ['Programming', 'Python']),
    ('Python Tricks', 2017, 302, 270, 'ebook', True, 'Dan Bader', ['Programming', 'Python']),
    ('Two Scoops of Django', 2020, 532, 510, 'ebook', False, 'Daniel Roy Greenfeld', ['Programming', 'Python', 'Django']),
    ('Clean Code', 2008, 464, 450, 'paper', True, 'Robert C. Martin', ['Programming', 'Software Engineering']),
    ('The Pragmatic Programmer', 2019, 352, 480, 'audio', True, 'David Thomas', ['Programming', 'Software Engineering']),
    ('Refactoring', 2018, 448, 530, 'paper', False, 'Martin Fowler', ['Programming', 'Software Engineering']),
    ('Design Patterns', 1994, 395, 600, 'paper', True, 'Erich Gamma', ['Programming', 'Software Engineering']),
    ('Grokking Algorithms', 2016, 256, 300, 'ebook', True, 'Aditya Bhargava', ['Programming', 'Algorithms']),
    ('Code Complete', 2004, 960, 550, 'paper', False, 'Steve McConnell', ['Programming', 'Software Engineering']),
    ('Designing Data-Intensive Applications', 2017, 616, 620, 'paper', True, 'Martin Kleppmann', ['Programming', 'Software Engineering']),
    ('The Clean Coder', 2011, 256, 250, 'audio', True, 'Robert C. Martin', ['Programming', 'Software Engineering']),
    ('Atomic Habits', 2018, 320, 299, 'audio', True, 'James Clear', ['Self-help']),
    ('Sapiens', 2014, 498, 350, 'paper', True, 'Yuval Noah Harari', ['History']),
    ('The Mythical Man-Month', 1995, 336, 200, 'audio', False, 'Fred Brooks', ['Software Engineering']),
    ('Deep Work', 2021, 296, 280, 'ebook', True, 'Cal Newport', ['Self-help']),
    ('The Colour of Magic', 1983, 288, 240, 'paper', True, 'Terry Pratchett', ['Fantasy']),
    ('The Hobbit', 1937, 310, 320, 'paper', True, 'J.R.R. Tolkien', ['Fantasy']),
]

# get_or_create / update_or_create: the script can be run repeatedly without duplicates
authors = {}
for name, (birth_date, website) in authors_data.items():
    author, _ = Author.objects.update_or_create(name=name, defaults={'birth_date': birth_date})
    AuthorProfile.objects.update_or_create(author=author, defaults={'website': website})
    authors[name] = author

genres = {}
for name in genres_data:
    genre, _ = Genre.objects.get_or_create(name=name)
    genres[name] = genre

for i, (title, year, pages, price, fmt, available, author, genre_names) in enumerate(books_data, start=1):
    book, _ = Book.objects.update_or_create(
        slug=slugify(title),
        defaults={
            'title': title,
            'isbn': f'978{i:010d}',
            'published_year': date(year, 1, 1),
            'pages': pages,
            'price': price,
            'format': fmt,
            'is_available': available,
            'author': authors[author],
        },
    )
    book.genres.set([genres[name] for name in genre_names])
    BookGenre.objects.filter(book=book).update(is_primary=False)
    BookGenre.objects.filter(book=book, genre=genres[genre_names[0]]).update(is_primary=True)

print(f'Authors: {Author.objects.count()}, Genres: {Genre.objects.count()}, Books: {Book.objects.count()}')
