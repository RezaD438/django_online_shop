from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages


def messages_home(request):
    messages.success(request, 'This is success')
    messages.warning(request, 'This is warning')
    messages.error(request, 'This is error')
    return render(request, 'home.html')


# class HomePageView(TemplateView):
#     template_name = 'home.html'


class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.htm'
