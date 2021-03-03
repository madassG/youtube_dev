from youtubedev.celery import app
from bot.models import User
from channels.models import Channel
from channels.channel import youtube_request_channel


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
    Users = User.objects.all()
    for user in Users:
        channel_id = tmp_parcer(user.youtube)
        if channel_id[0] != 'NO':
            playlist_id = youtube_request_channel(channel_id[0], channel_id[1], 'contentDetails')
            user.playlist_id = playlist_id
            user.save()
            data = youtube_request_channel(channel_id[0], channel_id[1])
            new_data = Channel()
            new_data.owner = user
            if data.get('hiddenSubscriberCount', False):
                new_data.subscribers = -1
            else:
                new_data.subscribers = data.get('subscriberCount', -1)
            new_data.total_views = data.get('viewCount', -1)
            new_data.videos_quantity = data.get('videoCount', -1)
            new_data.save()


@app.task
def check_videos():
    Users = User.objects.all()
    for user in Users:
        playlist_id = playlist_parcer(user.playlist_id)
        if playlist_id != '':
            pass

