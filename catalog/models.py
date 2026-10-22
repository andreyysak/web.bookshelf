from datetime import date

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')
    website = models.URLField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return f'Profile of {self.author}'


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


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
    language = models.CharField(max_length=4, default='en')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    genres = models.ManyToManyField(Genre, through='BookGenre', related_name='books', blank=True)
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
            condition=Q(pages__gt=0),
            name='check_pages'
        )]


class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.book.title} {self.genre.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'genre'], name='unique_book_genre'),
            models.UniqueConstraint(fields=['book'], condition=Q(is_primary=True), name='unique_primary_genre')
        ]
