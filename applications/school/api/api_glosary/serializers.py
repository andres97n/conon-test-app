from rest_framework import serializers

from applications.school.models import Glosary, AsignatureClassroom


class GlosarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glosary
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create a Glosary
    def create(self, validated_data):
        if not AsignatureClassroom.objects.\
                asignature_classroom_exists(validated_data['asignature_classroom'].id):
            raise serializers.ValidationError(
                detail='Error, no se encuentra relación con este valor; consulte con el Administrador.'
            )
        glosary = Glosary(**validated_data)
        glosary.save()
        return glosary

    # Update Glosary
    def update(self, instance, validated_data):
        if instance.asignature_classroom != validated_data['asignature_classroom']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar la relación de este registro; '
                       'consulte con el Administrador.'
            )
        update_glosary = super().update(instance, validated_data)
        update_glosary.save()
        return update_glosary

    # Show Glosary Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'asignature_classroom': {
                'classroom': {
                    'id': instance.asignature_classroom.classroom.id,
                    'name': instance.asignature_classroom.classroom.__str__()
                },
                'asignature': {
                    'id': instance.asignature_classroom.asignature.id,
                    'name': instance.asignature_classroom.asignature.__str__()
                },
                'teacher': {
                    'id': instance.asignature_classroom.teacher.id,
                    'name': instance.asignature_classroom.teacher.__str__()
                }
            },
            'state': instance.state,
            'observations': instance.observations,
            'created_at': instance.created_at
        }
