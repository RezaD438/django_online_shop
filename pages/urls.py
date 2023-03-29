from django.urls import path

# from .views import HomePageView, AboutUsPageView
from .views import messages_home, AboutUsPageView

urlpatterns = [
    path('', messages_home, name='home'),
    path('aboutus/', AboutUsPageView.as_view(), name='aboutus'),
]
