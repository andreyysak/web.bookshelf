# Bookshelf

A book catalog web app built with Django. It is a learning project that I develop step by step to practice Django: routing, views, templates, models, the ORM, forms, class-based views and authentication.

> **Status: work in progress.** The catalog, book pages, reviews and user accounts work with seeded data. Tests and deployment are not done yet.

## What works now

- **Catalog:** paginated book list, search, filtering by genre, publication year and ISBN, book detail page with reviews and a buy box, author statistics built with ORM aggregation
- **Books management:** create, edit and delete books with model forms and class-based views (login required)
- **Reviews:** logged-in users can add a review with a rating from 1 to 5, and delete their own reviews
- **Accounts:** registration, login and logout, password change and password reset (emails are printed to the console in development)
- **Feedback form** with validation and flash messages
- **Models with relationships:** authors, author profiles (one-to-one), genres, books (foreign key and many-to-many through a model with a "primary genre" flag and a conditional unique constraint), stock and reviews, with database-level constraints
- **Optimized queries:** `select_related`, `prefetch_related` with `Prefetch`, `annotate` and `aggregate`, checked with Django Debug Toolbar
- Migrations, including hand-written data migrations
- Django admin for managing books, authors, genres and reviews
- Template inheritance with reusable components (book card, rating, breadcrumb, pagination, messages)
- SCSS styles compiled to CSS, static and media files
- A seed script that fills the database with sample authors, genres, books and reviews

## Planned

- Tests
- Custom user model, middleware and signals
- Caching
- REST API with Django REST framework
- Deployment

## Tech stack

- Python and [Django](https://www.djangoproject.com) 6
- SQLite
- Pillow (image fields)
- Django Debug Toolbar
- Django templates
- SCSS (compiled with Sass)

## Getting started

Requirements: Python 3 (and Node.js only if you want to change the styles).

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

Open http://127.0.0.1:8000/. To use the admin, create a superuser first:

```bash
python manage.py createsuperuser
```

and then go to http://127.0.0.1:8000/admin/.

To change the styles, install the dev dependency and recompile the SCSS:

```bash
npm install
npx sass --watch static/scss/main.scss static/css/main.css
```

## Project structure

```text
.
├── config/          # project settings and root URLs
├── catalog/         # books, authors, genres, stock: models, views, URLs, template tags
├── reviews/         # book reviews
├── accounts/        # registration
├── feedback/        # feedback form
├── templates/       # base template, pages, components, partials, auth pages
├── static/          # SCSS and compiled CSS
└── seed.py          # sample data
```

## Notes

This project is for learning and local development only. The settings use `DEBUG = True` and a development secret key, so they are not suitable for production.

## Author

Andrii Sak — frontend developer (React, Next.js, Vue) with backend experience in Python and Node.js.
[LinkedIn](https://www.linkedin.com/in/andrii-sak-4a3839329/) · [GitHub](https://github.com/andreyysak)
