from enum import Enum


class NotificationType(str, Enum):
    error = 'error'
    success = 'success'


def add_notification(request, n_type: NotificationType, n_text: str):
    n_obj = {
            'type': n_type,
            'text': n_text
    }
    if not request.session.get('notification'):
        request.session['notification'] = [n_obj]
    else:
        nots = request.session['notification']
        nots.append(n_obj)
        request.session['notification'] = nots
