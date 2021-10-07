from rest_framework import serializers

from applications.school.models import AsignatureClassroom, Classroom, Asignature
from applications.school.models import Teacher


class AsignatureClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignatureClassroom
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Validate Classroom Id
    def validate_classroom(self, value):
        if not Classroom.objects.is_active(value.id):
            raise serializers.ValidationError(f'Error, Aula [{value.id}] inexistente o inactiva.')
        return value

    # Validate Asignature Id
    def validate_asignature(self, value):
        if not Asignature.objects.is_active(value.id):
            raise serializers.ValidationError(f'Error, esta Asignatura [{value.id}] no existe.')
        return value

    # Validate Teacher Id
    def validate_teacher(self, value):
        if not Teacher.objects.is_active(value.id):
            raise serializers.ValidationError(f'Error, este Docente [{value.id}] no existe.')
        return value

    # Return Data
    def to_representation(self, instance):
        return dict(
            id=instance.id,
            classroom=dict(
                id=instance.classroom.id,
                name=instance.classroom.name,
            ),
            asignature=dict(
                id=instance.asignature.id,
                name=instance.asignature.name,
            ),
            teacher=dict(
                id=instance.teacher.id,
                name=instance.teacher.person.name,
                last_name=instance.teacher.person.last_name
            ),
            observations=instance.observations
        )
