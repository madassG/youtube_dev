from config.celery import app
from channels.models import Channel, Video, Account
from users.models import Client
from channels.channel import youtube_request_channel, youtube_request_playlist, youtube_request_video
from datetime import datetime, timedelta, timezone
from channels.analysis import channel_delay
import math
import logging

logger = logging.getLogger(__name__)


def playlist_parcer(id):
    return id


@app.task
def check_accounts():
    """ Task to send task for checking all the accounts """
    clients = Client.objects.all()
    for client in clients:
        if not client.subscription:
            continue

        freq = client.subscription.check_frequency
        now = datetime.now(tz=timezone(timedelta(hours=3), name='МСК'))
        if client.last_check is None or now - client.last_check > timedelta(hours=freq) or True:
            client.last_check = now - timedelta(minutes=30)
            client.save()
            for acc in client.accounts.all():
                check_user.delay(acc.pk)


@app.task
def check_videos():
    """ Creating task to check all video from the past week of every user """
    clients = Client.objects.all()
    for client in clients:
        sub = client.subscription
        for user in client.accounts.all():
            playlist_id = playlist_parcer(user.playlist_id)
            if playlist_id != '':
                response = youtube_request_playlist(playlist_id)
                try:
                    videos = response['items']
                    totalResults = response['pageInfo']['totalResults']
                    perPage = response['pageInfo']['resultsPerPage']
                except KeyError:
                    logger.error(
                        f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
                        f": check_videos - key error - playlist id: {playlist_id}"
                    )
                key = False
                for i in range(math.ceil(totalResults / perPage)):
                    if key:
                        break
                    if i != 0:
                        response = youtube_request_playlist(playlist_id, response['nextPageToken'])
                        if response is None:
                            logger.error(
                                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} "
                                f": check_videos - playlist id: {playlist_id}")
                            return
                        if 'items' not in response:
                            logger.error(
                                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} "
                                f": check_videos - playlist id: {playlist_id}")
                            return
                        videos = response['items']
                    for vid in videos:
                        pb_at_str = vid['contentDetails']['videoPublishedAt']
                        vid_id = vid['contentDetails']['videoId']
                        published_at = datetime.strptime(pb_at_str, '%Y-%m-%dT%H:%M:%SZ')
                        if (datetime.now() - published_at).days < sub.check_time:
                            check_video.delay(user.pk, vid_id)
                        else:
                            if (datetime.now() - published_at).days < sub.check_time_2:
                                v = Video.objects.filter(url_id=vid_id).order_by('-published_at')[:1]
                                if not v or v.published_at - datetime.now(tz=timezone(timedelta(hours=3), name='МСК')) \
                                        > timedelta(hours=sub.check_frequency_after_check_time):
                                    check_video.delay(user.pk, vid_id)
                                continue
                            key = True
                            break


@app.task
def check_video(user_id, video_id):
    """ Task to check video """
    user = Account.objects.get(pk=user_id)
    youtube_items = youtube_request_video(video_id)
    if youtube_items is None:
        logger.error(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} "
            f": check_video - video id: {video_id}")
        return
    if youtube_items is not None:
        video = Video()
        video.owner = user
        video.url_id = video_id
        video.published_at = datetime.strptime(youtube_items['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        video.avatar = youtube_items['snippet']['thumbnails']['medium']['url']
        video.title = youtube_items['snippet']['title']
        video.viewCount = youtube_items['statistics'].get('viewCount', -1)
        video.likeCount = youtube_items['statistics'].get('likeCount', -1)
        video.commentsCount = youtube_items['statistics'].get('commentCount', -1)
        video.save()


@app.task
def check_user(user_id):
    """ Task to check info about user """
    user = Account.objects.get(pk=user_id)
    channel_id = user.youtube
    is_username = False
    if channel_id:
        items = youtube_request_channel(channel_id, is_username)
        if items is None:
            user.youtube_error = True
            user.save()
            logger.error(
                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} "
                f": check_user - user id: {user_id}")
            return

        user.youtube_error = False
        user.save()
        user.playlist_id = items['contentDetails']['relatedPlaylists']['uploads']
        user.name = items['brandingSettings'].get('channel').get('title')
        user.channel_keywords = items['brandingSettings'].get('channel').get('keywords')
        user.channel_country = items['brandingSettings'].get('channel').get('country')
        user.banner_url = items['brandingSettings'].get('image').get('bannerExternalUrl')
        user.save()

        data = items['statistics']
        new_data = Channel()
        new_data.owner = user

        if data.get('hiddenSubscriberCount', False):
            new_data.subscribers = -1
        else:
            new_data.subscribers = data.get('subscriberCount', -1)

        new_data.total_views = data.get('viewCount', -1)
        new_data.videos_quantity = data.get('videoCount', -1)
        new_data.save()
        user.views_day = channel_delay(user_id, 1, False).get('change', 0).get('views', 0)
        user.views_week = channel_delay(user_id, 7, False).get('change', 0).get('views', 0)
        user.views_month = channel_delay(user_id, 30, False).get('change', 0).get('views', 0)
        user.views_quarter = channel_delay(user_id, 91, False).get('change', 0).get('views', 0)

        user.subs_day = channel_delay(user_id, 1, False).get('change', 0).get('subs', 0)
        user.subs_week = channel_delay(user_id, 7, False).get('change', 0).get('subs', 0)
        user.subs_month = channel_delay(user_id, 30, False).get('change', 0).get('subs', 0)
        user.subs_quarter = channel_delay(user_id, 91, False).get('change', 0).get('subs', 0)
        user.save()
