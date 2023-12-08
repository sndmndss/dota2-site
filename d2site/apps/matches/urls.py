from django.urls import path
from .views import MatchView

app_name = 'match'
urlpatterns = [
    path('<int:match_id>/', MatchView.as_view(), name='match'),
]
