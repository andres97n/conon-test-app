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

    # Create a AsignatureClassroom Data
    def create(self, validated_data):
        if not Classroom.objects.is_active(value.id):
            raise serializers.ValidationError(f'Error, Aula [{value.id}] inexistente o inactiva.')
        if not Asignature.objects.is_active(value.id):
            raise serializers.ValidationError(f'Error, esta Asignatura [{value.id}] no existe.')
        if not Teacher.objects.is_active(value.id):
            raise serializers.ValidationError(f'Error, este Docente [{value.id}] no existe.')
        asignature_classroom = AsignatureClassroom(**validated_data)
        asignature_classroom.save()
        return asignature_classroom

    # Update AsignatureClassroom
    def update(self, instance, validated_data):
        if instance.classroom != validated_data['classroom']:
            raise serializers.ValidationError(
                'Error, una vez ingresado el Aula no se puede cambiar el mismo.')
        if instance.asignature != validated_data['asignature']:
            raise serializers.ValidationError(
                'Error, una vez ingresada la Asignatura no se puede cambiar el mismo.')
        if instance.teacher != validated_data['teacher']:
            raise serializers.ValidationError(
                'Error, una vez ingresado el Docente no se puede cambiar el mismo.')
        update_asignature_classroom = super().update(instance, validated_data)
        update_asignature_classroom.save()
        return update_asignature_classroom

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
