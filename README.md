# Bookshelf

A book catalog web app built with Django. It is a learning project that I develop step by step to practice Django: URL routing, views, templates, models, migrations, the QuerySet API and the ORM.

> **Status: work in progress.** The catalog, search and detail pages work with seeded data. There is no user authentication yet, and the project is not deployed.

## What works now

- Book list, book detail, and filtering by genre, by publication year and by ISBN
- Monthly archive page (regular-expression URL) and a custom `isbn` URL path converter
- Search
- Author statistics page built with ORM aggregation
- Models with relationships: authors, author profiles (one-to-one), genres, books (foreign key and many-to-many through a model with a "primary genre" flag) and reviews
- Database migrations, including data migrations
- Django admin for managing books, authors, genres and reviews
- Template inheritance with reusable includes (book card, latest books)
- A seed script that fills the database with sample authors, genres, books and reviews
- Django Debug Toolbar for development

## Planned

- Advanced ORM queries and query optimization
- Forms and review submission
- Authentication
- Tests
- Deployment

## Tech stack

- Python and [Django](https://www.djangoproject.com) 6
- SQLite
- Pillow (image fields)
- Django Debug Toolbar
- Django templates

## Getting started

Requirements: Python 3.

```bash
git clone https://github.com/andreyysak/web.bookshelf.git
cd web.bookshelf
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < seed.py
python manage.py runserver
```

Open http://127.0.0.1:8000/books/. To use the admin, create a superuser first:

```bash
python manage.py createsuperuser
```

and then go to http://127.0.0.1:8000/admin/.

## Project structure

```text
.
├── config/          # project settings and root URLs
├── catalog/         # books, authors, genres: models, views, URLs, template tags
├── reviews/         # book reviews
├── templates/       # base template, catalog pages, includes
└── seed.py          # sample data
```

## Notes

This project is for learning and local development only. The settings use `DEBUG = True` and a development secret key, so they are not suitable for production.

## Author

Andrii Sak — frontend developer (React, Next.js, Vue) with backend experience in Python and Node.js.
[LinkedIn](https://www.linkedin.com/in/andrii-sak-4a3839329/) · [GitHub](https://github.com/andreyysak)
