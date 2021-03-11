from bot.models import User
from channels.models import Channel
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


def channel_delay(user_id, time=0):
    user = User.objects.get(pk=user_id)
    if time != 0:
        now = datetime.now().date()
        delta = timedelta(days=time)
        notes = Channel.objects.filter(owner=user).filter(created_at__date__gte=(now-delta)).order_by('created_at')
        behind_notes = Channel.objects.filter(owner=user).filter(created_at__date__gte=(now-delta)).order_by('-created_at')
        change = {
            'subs': behind_notes[0].subscribers - notes[0].subscribers,
            'vids': behind_notes[0].videos_quantity - notes[0].videos_quantity,
            'views': behind_notes[0].total_views - notes[0].total_views
        }
        notes_array = []
        for note in notes:
            notes_array.append(model_to_dict(note))

        result = {
            'notes': notes_array,
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
