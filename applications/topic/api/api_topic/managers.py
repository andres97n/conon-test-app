from datetime import datetime
from django.db import models


class TopicManager(models.Manager):

    def get_topic_list(self):
        return self.select_related('owner', 'classroom', 'asignature').filter(auth_state='A'). \
            order_by('-active', '-created_at')

    def get_topic_by_id(self, pk=None):
        try:
            return self.select_related('owner', 'classroom', 'asignature').\
                filter(
                    auth_state='A'
                ).get(id=pk)
        except None:
            return None

    def topic_exists(self, pk=None):
        return self.filter(id=pk, active=True, auth_state='A').exists()

    def get_topics_by_type(self, prototype=None):
        try:
            self.filter()
            return self.select_related('owner', 'owner__person', 'classroom', 'asignature'). \
                filter(
                    type=prototype, auth_state='A'
                ).order_by('-created_at', 'active')
        except:
            return None

    def get_many_topics(self, topics=None):
        try:
            if topics is not None:
                return list(self.in_bulk(topics).values())
            else:
                return None
        except:
            return None

    def get_students_by_topic_id(self, pk=None, active=None):
        try:
            if active is not None:
                return self.filter(
                    id=pk,
                    active=True,
                    auth_state='A',
                    students__auth_state='A'
                ).values(
                    'students',
                    'students__person__identification',
                    'students__person__name',
                    'students__person__last_name',
                    'students__person__age',
                    'students__person__user'
                )
            else:
                return self.filter(id=pk, auth_state='A').values(
                    'students',
                    'students__person__identification',
                    'students__person__name',
                    'students__person__last_name',
                    'students__person__age',
                    'students__person__user'
                )
        except:
            return None

    def get_topics_by_owner(self, user=None):
        try:
            return self.select_related('owner', 'classroom', 'asignature').filter(
                owner_id=user, active=True, auth_state='A'
            )
        except:
            return None

    def get_topic_by_id_active(self, pk=None):
        try:
            return self.select_related('owner', 'classroom', 'asignature').filter(
                id=pk,
                auth_state='A',
                active=True
            ).first()
        except None:
            return None

    def get_topics_by_students(self, student_id=None, period_id=None):
        try:
            return self.select_related('owner', 'classroom', 'asignature').\
                filter(
                students=student_id,
                classroom__school_period=period_id,
                classroom__state=1,
                classroom__auth_state='A',
                asignature__state=1,
                asignature__auth_state='A',
                active=True,
                auth_state='A'
            )
        except:
            return None

    def get_inactive_topics_by_student(self, student_id=None, period_id=None):
        try:
            return self.select_related('owner', 'classroom', 'asignature').\
                filter(
                students=student_id,
                classroom__school_period=period_id,
                classroom__state=1,
                classroom__auth_state='A',
                asignature__state=1,
                asignature__auth_state='A',
                active=False,
                auth_state='A'
            )
        except:
            return None

    def get_current_topics_by_students(self, student_id=None, period_id=None):
        try:
            return self.select_related('owner', 'classroom', 'asignature').\
                filter(
                students=student_id,
                classroom__school_period=period_id,
                classroom__state=1,
                classroom__auth_state='A',
                asignature__state=1,
                asignature__auth_state='A',
                active=True,
                auth_state='A',
                end_at__gte=datetime.now(),
            )
        except:
            return None
