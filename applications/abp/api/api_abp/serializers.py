from rest_framework import serializers

from applications.abp.models import Abp
from applications.topic.models import Topic


class AbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Topic Validation
    def validate_topic(self, value):
        if value.type != 2:
            raise serializers.ValidationError(
                {
                    'topic': 'No se puede crear este ABP, por favor revise el tipo seleccionado.'
                }
            )
        return value

    # State Validation
    def validate_state(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no existe este Nivel de Curso.'
                }
            )
        return value

    # Create ABP
    def create(self, validated_data):
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no se puede crear este Tema; consulte con el Administrador.'
                }
            )
        abp = Abp(**validated_data)
        abp.save()
        return abp

    # Update ABP
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no es posible editar este Tema; por favor consulte con el Administrador.'
                }
            )
        update_abp = super().update(instance, validated_data)
        update_abp.save()
        return update_abp

    # Return ABP Main Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'topic': {
                'id': instance.topic.id,
                'title': instance.topic.title,
            },
            'problem': instance.problem,
            'oral_explication': instance.oral_explication,
            'descriptive_image': instance.descriptive_image,
            'reference_url': instance.reference_url,
            'state': instance.state,
            'created_at': instance.created_at
        }
