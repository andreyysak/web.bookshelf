# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

A Django learning project: `Bookshelf`, the book catalog (authors, genres, reviews) built in **Part 1** of the course spec `~/Downloads/practice-django.md` (outside the repo). Part 1 has 29 sequential steps (01 intro … 29 deployment, covering admin, forms, CBVs, auth, custom user, middleware, signals, testing, caching, async, DRF along the way), each building on the previous one. **Part 2 of that file (`Gatherly`, the events/tickets platform) is a separate final project and is not part of this repo**, so don't use its requirements here.

- Each step has three tiers: **Основне** (required), **Ускладнення** (extra), **Перевір себе** (self-check questions). When working on a step, read that step's section in the spec first.
- One commit per step: `feat: step NN: <topic>` (or `wip:` while it's in progress). Work happens on `develop`; `main` is the PR target.
- `NOTES.md` holds the author's own answers (in Ukrainian) to the theory and self-check questions, with sections separated by `----` lines. Add to it; don't rewrite it.
- **This is a learning project: the user writes all the code.** Claude's role is mentor: track progress against the spec, explain concepts, give hints and guiding questions, and review the user's code. Don't implement course tasks or edit project code. Reply in Ukrainian. Item numbers like "10.9" mean step 10, item 9, counting the Основне items first and then the Ускладнення items.

## Commands

Uses a local virtualenv in `.venv` and SQLite (`db.sqlite3`, local and not tracked in git).

```bash
source .venv/bin/activate
pip install -r requirements.txt

python manage.py runserver                 # app lives under /books/, admin at /admin/
python manage.py makemigrations && python manage.py migrate
python manage.py shell < seed.py           # idempotent seed (update_or_create / get_or_create)

python manage.py test                      # all tests
python manage.py test catalog              # one app
python manage.py test catalog.tests.SomeTestCase.test_method   # single test
```

There is no linter/formatter configured. `catalog/tests.py` and `reviews/tests.py` are currently empty stubs.

## Architecture

- `config/` — project package (settings, root URLconf). Django 6.1, `LANGUAGE_CODE='uk'`, `TIME_ZONE='Europe/Kyiv'`, `django-debug-toolbar` enabled (needs `INTERNAL_IPS`, already set to 127.0.0.1). Media is served from `media/` in dev via `static()` in `config/urls.py`.
- `catalog/` — core domain: `Author`, `AuthorProfile` (1:1, `related_name='profile'`), `Genre`, `Book`, and `BookGenre`, the explicit `through` model for `Book.genres`. `BookGenre` enforces one primary genre per book via a conditional `UniqueConstraint`; genres are `PROTECT`ed, authors are `SET_NULL`. `Book` and `Genre` auto-fill `slug` in `save()`.
- `reviews/` — `Review` FK to `Book` (`related_name='reviews'`), rating constrained 1–5 both by validators and a DB `CheckConstraint`. It depends on `catalog`, never the other way round (except views importing `Review` for prefetching).
- URLs: all catalog routes are namespaced `catalog:` and mounted at `books/`. `catalog/converters.py` registers a custom `isbn` path converter (10 or 13 digits); `book-archive` uses `re_path` with named groups. Many views (detail, by-genre, by-year, isbn, archive) are still plain `HttpResponse` placeholders.
- ORM-heavy views (`book_list`, `book_search`, `author_stats`) are where the course's query-optimization work lives: `select_related('author')`, `prefetch_related('genres')`, `Prefetch(..., to_attr='good_reviews')`, and `annotate`/`aggregate` (note `Count(..., distinct=True)` when joining through reviews — `seed.py` data is deliberately shaped to expose that and `Avg → None` cases). Preserve these optimizations when editing; check query counts with the debug toolbar.
- `catalog/data.py` is a legacy in-memory `BOOKS` list from before models existed; it is still used by the `latest_books` inclusion tag in `catalog/templatetags/catalog_extras.py` (which also defines the `reading_time` filter).
- Templates live in the project-level `templates/` (`base.html`, `catalog/*`, `includes/*` partials), not in app directories.
- Migrations include hand-written ones (e.g. `catalog/migrations/0003_fill_empty_slugs.py` data migration, and the 0007/0008 switch of `Book.genres` to the `BookGenre` through model) — don't squash or regenerate them.
