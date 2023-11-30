from django.urls import path
from django.views.generic.base import RedirectView
from .views import HomeView

app_name = 'home'

urlpatterns = [
    path('', RedirectView.as_view(url='home/')),
    path('home/', HomeView.as_view(), name='home'),
]
