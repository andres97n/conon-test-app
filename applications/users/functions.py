from django.utils import timezone

from django.contrib.sessions.models import Session
from applications.users.models import Student, Teacher, User


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


# Validate if Person belongs to a Teacher or Student
def is_person_assigned(pk=None):
    teacher_validate, student_validate = None, None
    try:
        teacher_validate = Teacher.objects.select_related('person').filter(person__id=pk, auth_state='A')
    except:
        pass
    try:
        student_validate = Student.objects.select_related('person').filter(person_id=pk, auth_state='A')
    except:
        pass
    if teacher_validate or student_validate:
        return True

    return False


def user_validate(pk=None, type=None):
    users = None
    is_admin, is_teacher, is_student, is_valid = False, False, False, True

    try:
        users = User.objects.select_related('person').filter(
            person__id=pk,
            is_active=True,
            auth_state='A'
        ).values('type')
    except:
        pass

    if users:
        for user in users:
            if user['type'] == 0:
                is_admin = True
            elif user['type'] == 1:
                is_teacher = True
            elif user['type'] == 2:
                is_student = True

        # The student cannot be an admin or a teacher
        if is_student and type == 0:
            is_valid = False
        if is_student and type == 1:
            is_valid = False

        # The admin or the teacher cannot be an student
        if is_admin and type == 2:
            is_valid = False
        if is_teacher and type == 2:
            is_valid = False

    return is_valid
