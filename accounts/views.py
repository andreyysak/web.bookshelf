from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("catalog:book-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # type: ignore
        return response
