from rest_framework import serializers

from applications.users.models import User, Person


class AdminStudentSerializer(serializers.Serializer):
    identification_type = serializers.ChoiceField(
        choices=Person.IdentificationChoices,
        required=True
    )
    identification = serializers.CharField(
        required=True
    )
    name = serializers.CharField(
        required=True
    )
    last_name = serializers.CharField(
        required=True
    )
