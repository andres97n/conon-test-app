
from rest_framework import serializers

from applications.ac.models import Ac
from applications.topic.models import Topic


class AcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ac
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Topic Validation
    def validate_topic(self, value):
        if value.type != 3:
            raise serializers.ValidationError(
                {
                    'topic': 'No se puede crear esta metodología, por '
                             'favor revise el tipo seleccionado.'
                }
            )
        return value

    # State Validation
    def validate_state(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no existe este Nivel de Curso; consulte con el Administrador.'
                }
            )
        return value

    # Create AC
    def create(self, validated_data):
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no se puede crear este Tema; consulte con el Administrador.'
                }
            )
        ac = Ac(**validated_data)
        ac.save()
        return ac

    # Update AC
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no se puede cambiar la referencia de este Tema; por favor '
                             'consulte con el Administrador.'
                }
            )
        update_ac = super().update(instance, validated_data)
        update_ac.save()
        return update_ac

    # Return AC Main Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'topic': {
                'id': instance.topic.id,
                'title': instance.topic.title,
            },
            'real_problem': instance.real_problem,
            'context_video': instance.context_video,
            'contex_audio': instance.contex_audio,
            'state': instance.state,
            'created_at': instance.created_at
        }
