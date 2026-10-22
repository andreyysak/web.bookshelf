from django.urls import path, register_converter, re_path

from .converters import ISBNConverter
from . import views

app_name = 'catalog'

register_converter(ISBNConverter, 'isbn')

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('<int:pk>/', views.book_detail, name='book-detail'),
    path('genre/<slug:slug>/', views.books_by_genre, name='books-by-genre'),
    path('year/<int:year>/', views.books_by_year, name='books-by-year'),

    path('isbn/<isbn:isbn>/', views.book_by_isbn, name='book-by-isbn'),

    re_path(
        r'^archive/(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])/$',
        views.book_archive,
        name='book-archive',
    ),

    path('search/', views.book_search, name='book-search'),
    path('api/ping/', views.api_ping, name='api-ping'),
    path('debug/', views.debug, name='debug'),
    path('user/<int:pk>/', views.get_user, name='get-user'),

    path('stats/', views.author_stats, name='author-stats')
]
