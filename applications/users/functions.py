from django.utils import timezone

from django.contrib.sessions.models import Session


def close_sessions(user):
    session_closed = False
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    if all_sessions.exists():
        for session in all_sessions:
            session_data = session.get_decoded()
            if user.id == int(session_data.get('_auth_user_id')):
                session.delete()
                session_closed = True
    return session_closed
