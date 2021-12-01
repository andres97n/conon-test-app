import django_filters

from applications.topic.models import Topic
from applications.users.models import Teacher


class TopicFilterSet(django_filters.FilterSet):
    owner = django_filters.CharFilter(method='transform_teacher_to_user')

    def transform_teacher_to_user(self, queryset, name, value):
        if value:
            user = Teacher.objects.get_user_id_by_teacher(pk=value)
            if user is None:
                return queryset
            if user['person__user']:
                user_id = user['person__user']
                return queryset.filter(owner=user_id)
            else:
                return queryset
        else:
            return queryset

    class Meta:
        model = Topic
        fields = [
            'owner',
            'type',
            'active'
        ]
