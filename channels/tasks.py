from youtubedev.celery import app
from bot.models import User
from channels.models import Channel, Video
from channels.channel import youtube_request_channel, youtube_request_playlist, youtube_request_video
from datetime import datetime
import math
import logging

logger = logging.getLogger(__name__)


def tmp_parcer(url):
    result = 'NO'
    user = False
    if url.find('channel/') != -1:
        id_start = url.find('channel/') + 8
        result = url[id_start:]
    elif url.find('user/') != -1:
        user_start = url.find('user/') + 5
        result = url[user_start:]
        user = True
    return [result, user]


def playlist_parcer(id):
    return id


@app.task
def check_accounts():
    """ Task to send task for checking all the accounts """
    Users = User.objects.all()
    for user in Users:
        check_user.delay(user.pk)


@app.task
def check_videos():
    """ Creating task to check all video from the past week of every user """
    Users = User.objects.all()
    for user in Users:
        playlist_id = playlist_parcer(user.playlist_id)
        if playlist_id != '':
            response = youtube_request_playlist(playlist_id)
            videos = response['items']
            totalResults = response['pageInfo']['totalResults']
            perPage = response['pageInfo']['resultsPerPage']
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
                    videos = response['items']
                for vid in videos:
                    pb_at_str = vid['contentDetails']['videoPublishedAt']
                    published_at = datetime.strptime(pb_at_str, '%Y-%m-%dT%H:%M:%SZ')
                    if (datetime.now() - published_at).days < 7:
                        check_video.delay(user.pk, vid['contentDetails']['videoId'])
                    else:
                        key = True
                        break


@app.task
def check_video(user_id, video_id):
    """ Task to check video """
    user = User.objects.get(pk=user_id)
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
        video.viewCount = youtube_items['statistics']['viewCount']
        video.likeCount = youtube_items['statistics']['likeCount']
        video.dislikeCount = youtube_items['statistics']['dislikeCount']
        video.commentsCount = youtube_items['statistics']['commentCount']
        video.save()


@app.task
def check_user(user_id):
    """ Task to check info about user """
    user = User.objects.get(pk=user_id)
    channel_id = tmp_parcer(user.youtube)
    if channel_id[0] != 'NO':
        items = youtube_request_channel(channel_id[0], channel_id[1])
        if items is None:
            logger.error(
                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} "
                f": check_user - user id: {user_id}")
            return
        user.playlist_id = items['contentDetails']['relatedPlaylists']['uploads']
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
