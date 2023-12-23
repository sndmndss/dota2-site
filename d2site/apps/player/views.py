from django.shortcuts import render, redirect
from django.views import View
from d2site.apps.player.services import CommentService, PlayerService

# TODO: Another profile for owner


class PlayerView(View):

    async def get(self, request, account_id=None):
        if account_id:
            player_service = PlayerService(account_id)
            comments, comment_form, trusted = await player_service.get_player_profile(request)
            player_stats, player_name, match_history = await player_service.get_player_data()
            return render(request, 'player/index.html', {
                'player_stats': player_stats,
                'name': player_name,
                'match_history': match_history,
                'comment_form': comment_form,
                'comments': comments,
                'trusted': trusted
            })
        else:
            return await self.handle_top_player_request(request)

    async def post(self, request, account_id: int):
        comment_service = CommentService(account_id)
        success, response = await comment_service.handle_new_comment(request)
        if success:
            return redirect('player:player', account_id=account_id)
        else:
            return response

    @staticmethod
    async def handle_top_player_request(request):
        return render(request, 'top_players/index.html')
