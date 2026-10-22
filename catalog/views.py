from django.db.models.aggregates import Count, Avg, Min, Max
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch

from .models import Book, Author, Genre
from reviews.models import Review


def book_list(request):
    books = (Book.objects.order_by('-price', 'title').select_related('author')
             .prefetch_related('genres', Prefetch('reviews', queryset=Review.objects.filter(rating__gte=4), to_attr='good_reviews')).all())
    p = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'catalog/book_list.html', {'page_obj': page_obj})


def book_search(request):
    query = request.GET.get('q')

    if not query:
        return HttpResponseBadRequest('Query parameter "q" is required')

    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__name__icontains=query) | Q(isbn__icontains=query)).select_related(
        'author').prefetch_related('genres').all()
    context = {'books': books}

    return render(request, 'catalog/search_list.html', context)


def author_stats(request):
    stats = Author.objects.annotate(total=Count('books', distinct=True), avg=Avg('books__reviews__rating'))
    book_stats = Book.objects.aggregate(avg_price=Avg('price'), min_pages=Min('pages'), max_pages=Max('pages'))
    top_genres = Genre.objects.annotate(count=Count('books')).order_by('-count')[:3]

    return render(request, 'catalog/author_stats.html', {'stats': stats, 'book_stats': book_stats, 'top_genres': top_genres})


def book_detail(request, pk):
    return HttpResponse(f'Details of book: {pk}')


def books_by_genre(request, slug):
    return HttpResponse(f'Books of genre: {slug}')


def books_by_year(request, year):
    return HttpResponse(f'Books from: {year}')


def book_by_isbn(request, isbn):
    return HttpResponse(f'Book ISBN: {isbn}')


def book_archive(request, year, month):
    return HttpResponse(f'Book archive for {month} month of {year} year')


@require_http_methods(['GET'])
def api_ping(request):
    return JsonResponse({'status': 'ok', 'method': request.method})


def debug(request):
    if not settings.DEBUG:
        raise Http404()

    return JsonResponse({
        'method': request.method,
        'path': request.path,
        'ip-address': request.META.get('REMOTE_ADDR'),
        'user-agent': request.headers.get('User-Agent'),
        'get-params': request.GET
    })


def get_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    return HttpResponse(f'User: {user.username}')
