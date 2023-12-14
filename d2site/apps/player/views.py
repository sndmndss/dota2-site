from django.shortcuts import render
from django.views import View
from d2site.script.game_coordinator_interface import get_player_data
from d2site.script.steam_api_requests import SteamWebApi
from django.http import HttpResponse


class PlayerView(View):

    async def get(self, request, account_id=None):
        if account_id:
            try:
                player_stats, player_name = await get_player_data(account_id)
                match_history = await SteamWebApi.get_match_history(account_id)  # TODO: исключения для сценариев result.status
                return render(request, 'player/index.html',
                              {'player_stats': player_stats,
                               'name': player_name,
                               'match_history': match_history})
            except Exception as e:
                return HttpResponse("Request failed: " + str(e), status=401)
        else:
            return await self.handle_top_player_request(request)

    async def handle_top_player_request(self, request):
        return render(request, 'top_players/index.html')
