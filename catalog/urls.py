from django.urls import path, re_path, register_converter

from . import views
from .converters import ISBNConverter

app_name = "catalog"

register_converter(ISBNConverter, "isbn")

urlpatterns = [
    path("", views.BookListView.as_view(), name="book-list"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("genre/<slug:slug>/", views.books_by_genre, name="books-by-genre"),
    path("year/<int:year>/", views.books_by_year, name="books-by-year"),
    path("isbn/<isbn:isbn>/", views.book_by_isbn, name="book-by-isbn"),
    re_path(
        r"^archive/(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])/$",
        views.book_archive,
        name="book-archive",
    ),
    path("search/", views.book_search, name="book-search"),
    path("api/ping/", views.api_ping, name="api-ping"),
    path("debug/", views.debug, name="debug"),
    path("user/<int:pk>/", views.get_user, name="get-user"),
    path("stats/", views.author_stats, name="author-stats"),
    path("create/", views.BookCreateView.as_view(), name="book-create"),
    path("<int:pk>/edit/", views.BookUpdateForm.as_view(), name="book-edit"),
    path("<int:pk>/delete/", views.BookDeleteView.as_view(), name="book-delete"),
    path("about/", views.AboutView.as_view(), name="about"),
]
