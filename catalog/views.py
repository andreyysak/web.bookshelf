from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth.models import User


def book_list(request):
    return HttpResponse('Books list')


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


def book_search(request):
    query = request.GET.get('q')

    if not query:
        return HttpResponseBadRequest('Query parameter "q" is required')

    return HttpResponse(f'You searched: {query}')


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
