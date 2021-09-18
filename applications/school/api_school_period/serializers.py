from rest_framework import serializers

from applications.school.models import SchoolPeriod


class SchoolPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPeriod
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]
