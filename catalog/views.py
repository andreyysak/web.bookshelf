from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.db.models.aggregates import Avg, Count, Max, Min
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from reviews.models import Review

from .forms import BookForm, BookSearchForm
from .models import Author, Book, Genre


def book_list(request):
    books = (
        Book.objects.order_by("-price", "title")
        .select_related("author")
        .prefetch_related(
            "genres",
            Prefetch(
                "reviews",
                queryset=Review.objects.filter(rating__gte=4),
                to_attr="good_reviews",
            ),
        )
        .all()
    )
    p = Paginator(books, 8)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    return render(request, "catalog/book_list.html", {"page_obj": page_obj})


def book_search(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.select_related("author").prefetch_related("genres")

    if form.is_valid():
        q = form.cleaned_data.get("q")
        genre = form.cleaned_data.get("genre")
        from_year = form.cleaned_data.get("from_year")
        to_year = form.cleaned_data.get("to_year")
        from_price = form.cleaned_data.get("from_price")
        to_price = form.cleaned_data.get("to_price")

        if q:
            books = books.filter(
                Q(title__icontains=q)
                | Q(author__name__icontains=q)
                | Q(isbn__icontains=q)
            )
        if genre is not None:
            books = books.filter(genres=genre)
        if from_year is not None:
            books = books.filter(published_year__year__gte=from_year)
        if to_year is not None:
            books = books.filter(published_year__year__lte=to_year)
        if from_price is not None:
            books = books.filter(price__gte=from_price)
        if to_price is not None:
            books = books.filter(price__lte=to_price)

    context = {"books": books, "form": form}
    return render(request, "catalog/search_list.html", context)


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            form.save_m2m()
            return redirect(book)
    else:
        form = BookForm()

    return render(
        request, "catalog/book_form.html", {"form": form, "title": "New book"}
    )


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect(book)
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "catalog/book_form.html",
        {"form": form, "title": f"Edit: {book.title}"},
    )


def author_stats(request):
    stats = Author.objects.annotate(
        total=Count("books", distinct=True), avg=Avg("books__reviews__rating")
    )
    book_stats = Book.objects.aggregate(
        avg_price=Avg("price"), min_pages=Min("pages"), max_pages=Max("pages")
    )
    top_genres = Genre.objects.annotate(count=Count("books")).order_by("-count")[:3]

    return render(
        request,
        "catalog/author_stats.html",
        {"stats": stats, "book_stats": book_stats, "top_genres": top_genres},
    )


def book_detail(request, pk):
    return HttpResponse(f"Details of book: {pk}")


def books_by_genre(request, slug):
    return HttpResponse(f"Books of genre: {slug}")


def books_by_year(request, year):
    return HttpResponse(f"Books from: {year}")


def book_by_isbn(request, isbn):
    return HttpResponse(f"Book ISBN: {isbn}")


def book_archive(request, year, month):
    return HttpResponse(f"Book archive for {month} month of {year} year")


@require_http_methods(["GET"])
def api_ping(request):
    return JsonResponse({"status": "ok", "method": request.method})


def debug(request):
    if not settings.DEBUG:
        raise Http404()

    return JsonResponse(
        {
            "method": request.method,
            "path": request.path,
            "ip-address": request.META.get("REMOTE_ADDR"),
            "user-agent": request.headers.get("User-Agent"),
            "get-params": request.GET,
        }
    )


def get_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    return HttpResponse(f"User: {user.username}")
