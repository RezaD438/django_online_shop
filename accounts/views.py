from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomCreationForm


class SignUpView(CreateView):
    form_class = CustomCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
