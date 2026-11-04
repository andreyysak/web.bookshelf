from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Book

from .forms import ReviewForm


def review_create(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return redirect(book)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form, "book": book})
