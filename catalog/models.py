from datetime import date

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify


class Book(models.Model):
    class Format(models.TextChoices):
        PAPER = 'paper', 'Paper'
        EBOOK = 'ebook', 'Ebook'
        AUDIO = 'audio', 'Audio'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.DateField()
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    format = models.CharField(
        max_length=10,
        choices=Format.choices,
        default=Format.PAPER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[self.pk])

    @property
    def is_new(self):
        return date.today().year - self.published_year.year <= 2

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        indexes = [models.Index(fields=['published_year'])]
        constraints = [models.CheckConstraint(
            check=Q(pages__gt=0),
            name='check_pages'
        )]
