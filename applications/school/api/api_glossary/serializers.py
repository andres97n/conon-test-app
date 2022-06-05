from rest_framework import serializers

from applications.school.models import Glossary, Classroom


class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create a Glosary
    def create(self, validated_data):
        if not Classroom.objects.\
                exists_classroom(validated_data['classroom'].id):
            raise serializers.ValidationError(
                detail='Error, no se encuentra relación con este valor; consulte con el '
                       'Administrador.'
            )
        glosary = Glossary(**validated_data)
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
            'classroom': {
                'id': instance.classroom.id,
                'name': instance.classroom.__str__()
            },
            'state': instance.get_state_display(),
            'observations': instance.observations,
            'created_at': instance.created_at
        }
