from django.shortcuts import render
from django.views import View
from d2site.script.requester import request_data


class PlayerView(View):

    async def get(self, request, account_id):
        data, name = await request_data(account_id)
        return render(request, 'player/index.html', {'player_stats': data, 'name': name})
