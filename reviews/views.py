from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Book

from .forms import ReviewForm


@require_POST
def review_create(request, pk):
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.book = book
        review.save()
        messages.success(request, "Thanks! Your review was added.")
        return redirect(book)
    return render(
        request,
        "books/book_detail.html",
        {"book": book, "reviews": book.reviews.all(), "review_form": form},  # type: ignore
        status=400,
    )
