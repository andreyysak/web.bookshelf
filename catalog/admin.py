from decimal import Decimal

from django.contrib import admin
from django.db.models import F, Avg

from .models import Author, AuthorProfile, Genre, Book, BookGenre, Stock
from reviews.models import Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year', 'price', 'format', 'is_available', 'avg_rating')
    list_editable = ('price',)
    list_filter = ('genres', 'format', 'is_available')
    search_fields = ('title', 'isbn', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BookGenreInline, ReviewInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'description'),
        }),
        ('Деталі видання', {
            'fields': ('isbn', 'published_year', 'pages', 'format', 'language'),
        }),
        ('Продаж', {
            'fields': ('price', 'is_available'),
        }),
        ('Службове', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    actions = ['mark_as_unavailable', 'lower_the_price']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(avg=Avg('reviews__rating'))

    @admin.display(description='Avg rating', ordering='avg')
    def avg_rating(self, obj):
        if obj.avg is None:
            return '-'

        return round(obj.avg, 1)

    @admin.action(description='Позначити як недоступні')
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'Позначено як недоступні: {updated}')

    @admin.action(description='Знизити ціну на 10%%')
    def lower_the_price(self, request, queryset):
        updated = queryset.update(price=F('price') * Decimal('0.9'))
        self.message_user(request, f'Ціну знижено для книг: {updated}')


admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookGenre)
admin.site.register(Stock)
