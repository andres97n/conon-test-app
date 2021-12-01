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
        if not Classroom.objects.is_active(validated_data['classroom'].id):
            raise serializers.ValidationError(
                {
                    'classroom': 'Error, Aula inexistente o inactiva.'
                }
            )
        if not Asignature.objects.is_active(validated_data['asignature'].id):
            raise serializers.ValidationError(
                {
                    'asignature': 'Error, esta Asignatura no existe.'
                }
            )
        if not Teacher.objects.is_active(validated_data['teacher'].id):
            raise serializers.ValidationError(
                {
                    'teacher': 'Error, este Docente no existe.'
                }
            )
        asignature_classroom = AsignatureClassroom(**validated_data)
        asignature_classroom.save()
        return asignature_classroom

    # Update AsignatureClassroom
    def update(self, instance, validated_data):
        if instance.classroom != validated_data['classroom']:
            raise serializers.ValidationError(
                {
                    'classroom': 'Error, una vez ingresado el Aula no se puede cambiar el mismo.'
                }
            )
        if instance.asignature != validated_data['asignature']:
            raise serializers.ValidationError(
                {
                    'asignature': 'Error, una vez ingresada la Asignatura no se puede cambiar el mismo.'
                }
            )
        if instance.teacher != validated_data['teacher']:
            raise serializers.ValidationError(
                {
                    'teacher': 'Error, una vez ingresado el Docente no se puede cambiar el mismo.'
                }
            )
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
                name=instance.teacher.__str__(),
            ),
            observations=instance.observations
        )


class AsignatureClassroomByAsignature(serializers.ModelSerializer):
    class Meta:
        model = AsignatureClassroom
        include = [
            'id',
            'classroom',
            'teacher',
            'created_at'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'classroom': {
                'id': instance.classroom.id,
                'name': instance.classroom.name,
            },
            'teacher': {
                'id': instance.teacher.id,
                'name': instance.teacher.__str__()
            },
            'created_at': instance.created_at
        }
