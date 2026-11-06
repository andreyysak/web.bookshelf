from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "input"}),
            "text": forms.Textarea(attrs={"rows": 4, "class": "textarea"}),
        }
