from django.contrib import messages
from django.shortcuts import render, redirect

from feedback.forms import FeedbackForm


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message')
            return redirect('feedback:feedback-send')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback.html', {'form': form})
