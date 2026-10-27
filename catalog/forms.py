from decimal import Decimal
from typing import Any

from django import forms

from .models import Genre


class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=50, required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.order_by('name'), empty_label='All genres', required=False)
    from_year = forms.IntegerField(min_value=1000, max_value=2100, required=False)
    to_year = forms.IntegerField(min_value=1000, max_value=2100, required=False)
    from_price = forms.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal('0'), required=False)
    to_price = forms.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal('0'), required=False)

    def clean(self):
        cleaned_data = super().clean()
        from_price = cleaned_data.get('from_price')
        to_price = cleaned_data.get('to_price')
        from_year = cleaned_data.get('from_year')
        to_year = cleaned_data.get('to_year')

        if from_price is not None and to_price is not None and from_price > to_price:
            self.add_error('from_price', '"From" price must not exceed "To" price')

        if from_year is not None and to_year is not None and from_year > to_year:
            self.add_error('from_year', '"From" year must not be greater than "To" year')

        return cleaned_data
