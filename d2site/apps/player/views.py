from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from d2site.script.game_coordinator_interface import get_player_data
from d2site.script.steam_api_requests import SteamWebApi
from django.http import HttpResponse
from .forms import CommentForm
from d2site.apps.home.models import SteamUser
from social_django.models import UserSocialAuth
from asgiref.sync import sync_to_async
# TODO: optimise, exceptions, refactor.


class PlayerView(View):

    async def get(self, request, account_id=None):
        if account_id:
            comment_form = CommentForm()
            profile_owner, created = await sync_to_async(SteamUser.objects.get_or_create, thread_sensitive=True)(
                steamID3=account_id)
            comments = await sync_to_async(list)(profile_owner.comments.all())
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
        is_authenticated = await sync_to_async(lambda: request.user.is_authenticated, thread_sensitive=True)()
        if is_authenticated:
            try:
                steam_user = await (sync_to_async(SteamUser.objects.get, thread_sensitive=True)
                                    (user_social_auth__user_id=request.user.id))
                steamID3 = steam_user.steamID3
                user_social = await (sync_to_async(UserSocialAuth.objects.get, thread_sensitive=True)
                                    (user_id=request.user.id))
                author_name = user_social.extra_data.get('player', {}).get('personaname', None)

            except SteamUser.DoesNotExist:
                pass
            profile_owner = await sync_to_async(get_object_or_404, thread_sensitive=True)(SteamUser, steamID3=account_id)
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = await sync_to_async(comment_form.save, thread_sensitive=True)(commit=False)
                new_comment.steam_users = profile_owner
                new_comment.author_uid = steamID3
                new_comment.author_name = author_name
                await sync_to_async(new_comment.save, thread_sensitive=True)()
                return redirect('player:player', account_id=account_id)
        else:
            return HttpResponse("logg in!", status=401)

    async def handle_top_player_request(self, request):
        return render(request, 'top_players/index.html')
