from django.urls import path

from applications.users.api.api_student.api import (get_student_by_user,
                                                    get_user_conversation_for_student)
from applications.users.api.api_conversation.api import (get_user_messages_count,
                                                         get_user_conversations_list)

urlpatterns = [
    path(
        r"student/student-conversation/<int:user>/<int:school_period>/",
        get_user_conversation_for_student,
        name="student_conversation"
    ),
    path(
        r"student/user/<int:user>/",
        get_student_by_user,
        name="student_by_user"
    ),
    path(
        r"conversation/user-messages-count/<int:user>/",
        get_user_messages_count,
        name="conversation_user_messages"
    ),
    path(
        r"conversation/user-conversations/<int:user>/<str:search>/",
        get_user_conversations_list,
        name="conversation_user-list"
    ),
]
