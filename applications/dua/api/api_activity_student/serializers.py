from rest_framework import serializers

from applications.dua.models import ActivityStudent, Activity
from applications.users.models import User


class ActivityStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStudent
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validate Qualification
    def validate_qualification(self, value):
        if value < 0:
            raise serializers.ValidationError(
                detail='Error, la Calificación no puede tener un valor menor que 0.'
            )

        return value

    # Create Data
    def create(self, validated_data):
        if not Activity.objects. \
                activity_exists(validated_data['activity'].id):
            raise serializers.ValidationError(
                detail='Error, no se pudo guardar su respuesta; '
                       'por favor consulte con el Administrador.'
            )
        if not User.objects. \
                user_exists(validated_data['owner'].id):
            raise serializers.ValidationError(
                detail='Error, Usuario inválido; por favor consulte con el Administrador.'
            )
        activity_student = ActivityStudent(**validated_data)
        activity_student.save()
        return activity_student

    # Update Question
    def update(self, instance, validated_data):
        if instance.activity != validated_data['activity']:
            raise serializers.ValidationError(
                detail='Error, no se puede editar esta Respuesta; '
                       'por favor consulte con el Administrador '
            )
        update_activity_student = super().update(instance, validated_data)
        update_activity_student.save()
        return update_activity_student

    # Get Data List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'activity': {
                'id': instance.activity.id,
                'description': instance.activity.description
            },
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__()
            },
            'qualification': instance.qualification,
            'observation': instance.observation,
            'created_at': instance.created_at
        }
