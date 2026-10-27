from django import forms
from django.core.exceptions import ValidationError

FEEDBACK_TOPIC_CHOICES = (
    ('general', 'General question'),
    ('site_bug', 'Website bug'),
    ('book_data', 'Incorrect book data'),
    ('book_suggestion', 'Suggest a book'),
    ('cooperation', 'Cooperation'),
    ('review_complaint', 'Report a review'),
)


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    topic = forms.ChoiceField(choices=FEEDBACK_TOPIC_CHOICES)
    company = forms.CharField(max_length=100, required=False)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        if not len(message) > 19:
            raise ValidationError('Message must be at least 20 characters')
        elif any(link in message.lower() for link in ('http://', 'https://', 'www.')):
            raise ValidationError('Links are not allowed')
        return message

    def clean(self):
        cleaned_data = super().clean()
        topic = cleaned_data.get('topic')
        company = cleaned_data.get('company')

        if topic == 'cooperation' and not company:
            self.add_error('company', 'Company is required for cooperation requests')

        return cleaned_data
