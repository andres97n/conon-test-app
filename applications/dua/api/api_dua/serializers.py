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

    # Validate Images
    def validate_images(self, value):
        if len(value) != 2:
            raise serializers.ValidationError(
                {
                    'images': 'Error, se deben mandar dos imágenes; consulte con el Administrador.'
                }
            )
        return value

    # Validate State
    def validate_state(self, value):
        if value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no se puede asignar este Estado a este metodología.'
                }
            )
        return value

    # Create DUA
    def create(self, validated_data):
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no se puede crear este Tema; consulte con el Administrador.'
                }
            )
        dua = Dua(**validated_data)
        dua.save()
        return dua

    # Update DUA
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no es posible editar este Tema; '
                             'por favor consulte con el Administrador.'
                }
            )
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


class DuaStudentsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        print(instance)
        return {
            'id': instance['students'],
            'person': {
                'identification': instance.person.identification,
                'name': f'{instance.person.name} {instance.person.last_name}',
            },
            'user': {
                'id': instance['person__user__id'],
                'email': instance['person__user__email']
            }
        }

