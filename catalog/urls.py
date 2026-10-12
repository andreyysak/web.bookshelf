from django.http import HttpResponse
from django.urls import path, register_converter, re_path

from .converters import ISBNConverter

app_name = 'catalog'

register_converter(ISBNConverter, 'isbn')

urlpatterns = [
    path('', lambda request: HttpResponse('Books list'), name='book-list'),
    path('<int:pk>/', lambda request, pk: HttpResponse(f'Book detail: {pk}'), name='book-detail'),
    path('genre/<slug:slug>/', lambda request, slug: HttpResponse(f'Books of genre: {slug}'), name='books-by-genre'),
    path('year/<int:year>/', lambda request, year: HttpResponse(f'Books for year: {year}'), name='books-by-year'),

    path('isbn/<isbn:isbn>/', lambda request, isbn: HttpResponse(f'Book ISBN: {isbn}'), name='book-by-isbn'),

    re_path(
        r'^archive/(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])/$',
        lambda request, year, month: HttpResponse(f'Archive: {year}-{month}'),
        name='book-archive',
    ),
]