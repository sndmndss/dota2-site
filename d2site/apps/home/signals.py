from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from .models import SteamUser
from d2site.scripts.helpers import steamid_to_steamid3
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=UserSocialAuth)
def create_or_update_steam_user_data(sender, instance, created, **kwargs):
    if instance.provider == 'steam' and instance.extra_data.get('player', {}):
        player_data = instance.extra_data.get('player', {})
        steamid64 = int(player_data.get('steamid'))
        if steamid64:
            steam_id3 = steamid_to_steamid3(steamid64)
            SteamUser.objects.update_or_create(
                user_social_auth=instance,
                defaults={'steamID3': steam_id3}
            )
    else:
        logger.info('Waining for extra data')


