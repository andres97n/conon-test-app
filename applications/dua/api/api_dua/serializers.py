from rest_framework import serializers

from applications.dua.models import Dua
from applications.topic.models import Topic


class DuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dua
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create DUA
    def create(self, validated_data):
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            raise serializers.ValidationError(
                detail='Error, no se puede crear este Tema; consulte con el Administrador.'
            )
        dua = Dua(**validated_data)
        dua.save()
        return dua

    # Update DUA
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            raise serializers.ValidationError('Error, no es posible editar este Tema; '
                                              'por favor consulte con el Administrador.')
        update_dua = super().update(instance, validated_data)
        update_dua.save()
        return update_dua

    # Return DUA Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'topic': {
                'id': instance.topic.id,
                'title': instance.topic.title
            },
            'written_conceptualization': instance.written_conceptualization,
            'oral_conceptualization': instance.oral_conceptualization,
            'example': instance.example,
            'video': instance.video,
            'images': instance.images,
            'extra_information': instance.extra_information,
            'observations': instance.observations,
            'created_at': instance.created_at
        }
