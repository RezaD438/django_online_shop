from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages


def messages_home(request):
    return render(request, 'pages/home.html')


# class HomePageView(TemplateView):
#     template_name = 'home.html'


class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.htm'
