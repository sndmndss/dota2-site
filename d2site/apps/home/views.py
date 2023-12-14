from django.shortcuts import render
from django.views import View
from d2site.apps.home.models import SteamUser


class HomeView(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            steam_user = SteamUser.objects.get(user_social_auth__user=request.user)
            player_nickname = steam_user.user_social_auth.extra_data.get('player', {}).get('personaname', '')
            steamid3 = steam_user.steamID3
            context['player_nickname'] = player_nickname
            context['steamid3'] = steamid3
        return render(request, 'home/index.html', context=context)
