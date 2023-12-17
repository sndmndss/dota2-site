from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from d2site.script.game_coordinator_interface import get_player_data
from d2site.script.steam_api_requests import SteamWebApi
from django.http import HttpResponse
from .forms import CommentForm
from d2site.apps.home.models import SteamUser
from asgiref.sync import sync_to_async


class PlayerView(View):

    async def get(self, request, account_id=None):
        if account_id:
            comment_form = CommentForm()
            profile_owner = await sync_to_async(get_object_or_404)(SteamUser, steamID3=account_id)
            comments = await sync_to_async(list, thread_sensitive=True)(profile_owner.comments.filter())
            try:
                player_stats, player_name = await get_player_data(account_id)
                match_history = await SteamWebApi.get_match_history(account_id)
                return render(request, 'player/index.html',
                              {'player_stats': player_stats,
                               'name': player_name,
                               'match_history': match_history,
                               'comment_form': comment_form,
                               'comments': comments})
            except Exception as e:
                return HttpResponse("Request failed: " + str(e), status=401)
        else:
            return await self.handle_top_player_request(request)

    async def post(self, request, account_id: int):
        profile_owner = await sync_to_async(get_object_or_404, thread_sensitive=True)(SteamUser, steamID3=account_id)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = await sync_to_async(comment_form.save, thread_sensitive=True)(commit=False)
            new_comment.steam_users = profile_owner
            await sync_to_async(new_comment.save, thread_sensitive=True)()
            return redirect('player:player', account_id=account_id)

    async def handle_top_player_request(self, request):
        return render(request, 'top_players/index.html')
