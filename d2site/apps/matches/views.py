from django.shortcuts import render
from django.views import View
from d2site.script.steam_api_requests import SteamWebApi


class MatchView(View):

    async def get(self, request, match_id):
        data = await SteamWebApi.get_match_details(match_id)
        return render(request, 'match/index.html', {'matches': data})
