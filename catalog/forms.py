from datetime import date
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Genre


def _style_fields(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            continue
        css = "select" if isinstance(widget, forms.Select) else "input"
        if isinstance(widget, forms.Textarea):
            css = "textarea"
        widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css}".strip()


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_fields(self)

    def clean_published_year(self):
        pub_year = self.cleaned_data["published_year"]
        now_date = date.today()

        if pub_year > now_date:
            raise ValidationError("Published year can not be in future")

        return pub_year

    class Meta:
        model = Book
        fields = [  # noqa: RUF012
            "title",
            "description",
            "isbn",
            "published_year",
            "pages",
            "price",
            "is_available",
            "format",
            "language",
            "author",
            "genres",
            "cover",
        ]
        widgets = {  # noqa: RUF012
            "published_year": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "description": forms.Textarea(attrs={"rows": 6}),
        }


class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=50, required=False)
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.order_by("name"),
        empty_label="All genres",
        required=False,
    )
    from_year = forms.IntegerField(min_value=1000, max_value=2100, required=False)
    to_year = forms.IntegerField(min_value=1000, max_value=2100, required=False)
    from_price = forms.DecimalField(
        max_digits=6, decimal_places=2, min_value=Decimal(0), required=False
    )
    to_price = forms.DecimalField(
        max_digits=6, decimal_places=2, min_value=Decimal(0), required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        from_price = cleaned_data.get("from_price")
        to_price = cleaned_data.get("to_price")
        from_year = cleaned_data.get("from_year")
        to_year = cleaned_data.get("to_year")

        if from_price is not None and to_price is not None and from_price > to_price:
            self.add_error("from_price", '"From" price must not exceed "To" price')

        if from_year is not None and to_year is not None and from_year > to_year:
            self.add_error(
                "from_year", '"From" year must not be greater than "To" year'
            )

        return cleaned_data
