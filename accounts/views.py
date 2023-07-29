from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .forms import CustomCreationForm


class SignUpView(generic.CreateView):
    form_class = CustomCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')
