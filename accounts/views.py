from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('teachhub:textbook_list')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # self.objectにsave()が格納される
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
