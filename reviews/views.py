from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView

from catalog.models import Book

from .forms import ReviewForm
from .models import Review


@login_required
@require_POST
def review_create(request, pk):
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.book = book
        review.user = request.user
        review.save()
        messages.success(request, "Thanks! Your review was added.")
        return redirect(book)
    return render(
        request,
        "books/book_detail.html",
        {"book": book, "reviews": book.reviews.select_related("user"), "review_form": form},  # type: ignore
        status=400,
    )


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "reviews/review_confirm_delete.html"

    def get_queryset(self):
        return Review.objects.select_related("book", "user")

    def test_func(self):
        review = self.get_object()
        user = self.request.user
        is_author = review.user_id is not None and review.user_id == user.pk
        return is_author or user.has_perm("reviews.delete_review")

    def get_success_url(self):
        return self.object.book.get_absolute_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your review was deleted.")
        return response
