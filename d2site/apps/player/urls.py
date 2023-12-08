from django.urls import path
from .views import PlayerView

app_name = 'player'
urlpatterns = [
    path('<int:account_id>/', PlayerView.as_view(), name='player'),
    path('', PlayerView.as_view(), name='top_players'),
]
