from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from catalog.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book} — {self.rating}/5'

    class Meta:
        ordering = ['-created_at']
        constraints = [models.CheckConstraint(
            check=Q(rating__gte=1, rating__lte=5),
            name='check_rating'
        )]
