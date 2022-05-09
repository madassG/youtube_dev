from bot.models import User
from channels.models import Channel, Video, Account
from datetime import datetime, timedelta
from django.forms.models import model_to_dict


def analyse_channel(user_id):
    changes = {
        'today': channel_delay(user_id),
        'day': channel_delay(user_id, 1),
        'week': channel_delay(user_id, 7),
        'month': channel_delay(user_id, 30),
        'quarter': channel_delay(user_id, 91),
    }
    return changes


def channel_delay(user_id, time=0, need_notes=True):
    user = Account.objects.get(pk=user_id)
    if time != 0:
        now = datetime.now().date()
        delta = timedelta(days=time)
        notes = Channel.objects.filter(owner=user).filter(created_at__date__gte=(now-delta)).order_by('created_at')
        behind_notes = Channel.objects.filter(owner=user).filter(created_at__date__gte=(now-delta)).order_by('-created_at')
        if notes:
            change = {
                'subs': behind_notes[0].subscribers - notes[0].subscribers,
                'vids': behind_notes[0].videos_quantity - notes[0].videos_quantity,
                'views': behind_notes[0].total_views - notes[0].total_views
            }
        else:
            change = {
                'subs': 0,
                'vids': 0,
                'views': 0
            }

        if need_notes:
            notes_array = {
                'values': {
                    'subs': [],
                    'vids': [],
                    'views': [],
                },
                'dates': []
            }
            for note in notes:
                notes_array['values']['subs'].append(note.subscribers)
                notes_array['values']['vids'].append(note.videos_quantity)
                notes_array['values']['views'].append(note.total_views)
                notes_array['dates'].append(datetime.strftime(note.created_at.date(), '%Y-%m-%d'))
            result = {
                'notes': notes_array,
                'change': change,
            }
        else:
            result = {
                'change': change,
            }
        return result
    else:
        notes = Channel.objects.filter(owner=user).order_by('-created_at')
        if notes:
            change = {
                'subs': notes[0].subscribers,
                'vids': notes[0].videos_quantity,
                'views': notes[0].total_views,
            }
            return change
        return None


def video_data(user_id):
    user = Account.objects.get(pk=user_id)
    videos = Video.objects.filter(owner=user).order_by('-published_at')
    ids = []
    for video_id in videos.values('url_id'):
        ids.append(video_id['url_id'])
    unique_ids = [e for i, e in enumerate(ids) if ids.index(e) == i]
    videos = []
    for video in unique_ids:
        video_dict = video_get_dict(video)
        videos.append(video_dict)
    return videos


def video_get_dict(video_id):
    vids = Video.objects.filter(url_id=video_id).order_by('created_at')
    data = vids[0]
    # print(data.title)
    query_changes = vids.values('viewCount', 'likeCount', 'dislikeCount', 'commentsCount', 'created_at')
    changes = []
    for change in query_changes:
        changes.append({
            'views': change['viewCount'],
            'likes': change['likeCount'],
            'dlikes': change['dislikeCount'],
            'comms': change['commentsCount'],
            'date': change['created_at'].date()
        })
    video_dict = {
        'url': 'https://www.youtube.com/watch?v=' + data.url_id,
        'publish_date': data.published_at,
        'end': data.created_at,
        'avatar': data.avatar,
        'title': data.title,
        'changes': changes,
    }

    return video_dict
