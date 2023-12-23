from django.urls import path
from .views import MatchView

urlpatterns = [
    path('<int:match_id>/', MatchView.as_view(), name='match'),
]
