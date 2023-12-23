from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from d2site.apps.home.models import SteamUser
from d2site.apps.player.forms import CommentForm
from d2site.scripts.steam_api_requests import SteamWebApi
from d2site.scripts.game_coordinator_interface import get_player_statistic
from django.contrib.auth import get_user
from social_django.models import UserSocialAuth
from django.http import Http404


async def _get_requester_steamid3(request):
    user = await sync_to_async(get_user)(request)
    steam_user = await (sync_to_async(SteamUser.objects.get, thread_sensitive=True)
                        (user_social_auth__user_id=user.id))
    requester_steamid3 = steam_user.steamID3
    return requester_steamid3


async def _user_is_authed(request):
    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated, thread_sensitive=True)()
    return is_authenticated


class PlayerService:
    def __init__(self, account_id):
        self.account_id = account_id

    async def get_player_profile(self, request):
        if await SteamWebApi.player_exists(self.account_id):
            trusted_commentator = False
            comment_form = None
            profile_owner, created = await sync_to_async(SteamUser.objects.get_or_create, thread_sensitive=True)(
                steamID3=self.account_id)
            comments = await sync_to_async(list)(profile_owner.comments.all().order_by('-created'))
            requester_steamid3 = await _get_requester_steamid3(request)
            if await _user_is_authed(request):
                matches_ids = await SteamWebApi.get_common_matches(self.account_id, requester_steamid3)
                comment_form = CommentForm()
                if not matches_ids:
                    return comments, comment_form, trusted_commentator
                else:
                    comment_form.fields['match_id'].choices = matches_ids
            trusted_commentator = True
            return comments, comment_form, trusted_commentator
        else:
            raise Http404("Игрок не найден")

    async def get_player_data(self):
        player_stats = await get_player_statistic(self.account_id)
        player_name = await SteamWebApi.get_player_name(self.account_id)
        match_history = await SteamWebApi.get_match_history(self.account_id)
        return player_stats, player_name, match_history


class CommentService:
    def __init__(self, account_id):
        self.account_id = account_id

    async def handle_new_comment(self, request):
        if await _user_is_authed(request):
            steamid3 = await _get_requester_steamid3(request)
            user_social = await (sync_to_async(UserSocialAuth.objects.get, thread_sensitive=True)
                                 (user_id=request.user.id))
            author_name = user_social.extra_data.get('player', {}).get('personaname', None)
            profile_owner = await sync_to_async(get_object_or_404, thread_sensitive=True)(SteamUser,
                                                                                          steamID3=self.account_id)
            matches_ids = await SteamWebApi.get_common_matches(self.account_id, steamid3)
            comment_form = CommentForm(data=request.POST)
            comment_form.fields['match_id'].choices = matches_ids
            if comment_form.is_valid():
                new_comment = await sync_to_async(comment_form.save, thread_sensitive=True)(commit=False)
                new_comment.steam_users = profile_owner
                new_comment.author_uid = steamid3
                new_comment.author_name = author_name
                await sync_to_async(new_comment.save, thread_sensitive=True)()
                return True, None
            else:
                return False, comment_form.errors
        else:
            return False, "User is not authenticated"
