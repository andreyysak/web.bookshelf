from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Prefetch, Q
from django.db.models.aggregates import Avg, Count, Max, Min
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from reviews.forms import ReviewForm
from reviews.models import Review

from .forms import BookForm, BookSearchForm
from .models import Author, Book, Genre


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    paginate_by = 10
    context_object_name = "books"

    def get_queryset(self):
        qs = (
            Book.objects.select_related("author")
            .prefetch_related(
                "genres",
                Prefetch(
                    "reviews",
                    queryset=Review.objects.filter(rating__gte=4),
                    to_attr="good_reviews",
                ),
            )
            .order_by("-created_at")
        )
        q = self.request.GET.get("q")
        genre = self.request.GET.get("genre")
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(author__name__icontains=q)
                | Q(isbn__icontains=q)
            )
        if genre:
            qs = qs.filter(genres__slug=genre)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["genres"] = Genre.objects.all()
        context["genre"] = self.request.GET.get("genre", "")
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"

    def get_queryset(self):
        return Book.objects.select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context["book"]
        context["reviews"] = book.reviews.select_related("user")
        context["review_form"] = ReviewForm()
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create book"
        return context


class BookUpdateForm(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update book"
        return context


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("catalog:book-list")


class AboutView(TemplateView):
    template_name = "catalog/about.html"


def book_search(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.select_related("author").prefetch_related(
        "genres",
        Prefetch(
            "reviews",
            queryset=Review.objects.filter(rating__gte=4),
            to_attr="good_reviews",
        ),
    )

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

    context = {
        "books": books,
        "form": form,
        "q": request.GET.get("q", ""),
    }
    return render(request, "books/book_search.html", context)


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
        "books/author_stats.html",
        {"stats": stats, "book_stats": book_stats, "top_genres": top_genres},
    )


def books_by_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    books = (
        Book.objects.filter(genres=genre)
        .select_related("author")
        .prefetch_related(
            "genres",
            Prefetch(
                "reviews",
                queryset=Review.objects.filter(rating__gte=4),
                to_attr="good_reviews",
            ),
        )
    )
    return render(request, "books/book_genre.html", {"genre": genre, "books": books})


def books_by_year(request, year):
    books = (
        Book.objects.filter(published_year__year=year)
        .select_related("author")
        .prefetch_related(
            "genres",
            Prefetch(
                "reviews",
                queryset=Review.objects.filter(rating__gte=4),
                to_attr="good_reviews",
            ),
        )
    )
    return render(request, "books/book_year.html", {"year": year, "books": books})


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
