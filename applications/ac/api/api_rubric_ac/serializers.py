
from rest_framework import serializers

from applications.ac.models import RubricAc, Ac


class RubricAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validate State
    def validate_state(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, el estado envíado no puede tener ese valor; '
                             'consulte con el Administrador.'
                }
            )
        return value

    # Create Rubric AC
    def create(self, validated_data):
        if not Ac.objects.exists_ac_methodology(validated_data['ac'].id):
            raise serializers.ValidationError(
                {
                    'ac': 'Error, la metodología ingresada no es válida; '
                          'consulte con el Administrador.'
                }
            )
        rubric_ac = RubricAc(**validated_data)
        rubric_ac.save()
        return rubric_ac

    # Update Rubric AC
    def update(self, instance, validated_data):
        if instance.ac != validated_data['ac']:
            raise serializers.ValidationError(
                {
                    'ac': 'Error, no se puede cambiar de pertenencia; '
                          'por favor consulte con el Administrador.'
                }
            )
        update_rubric_ac = super().update(instance, validated_data)
        update_rubric_ac.save()
        return update_rubric_ac


class RubricAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Rubric Ac List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'ac': {
                'id': instance.ac.id,
                'real_problem': instance.ac.real_problem,
                'topic': {
                    'id': instance.ac.topic.id,
                    'title': instance.ac.topic.title
                },
            },
            'description_rubric': instance.description_rubric,
            'ac_final_value': instance.ac_final_value,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }


class RubricAcShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'description_rubric': instance.description_rubric,
            'ac_final_value': instance.ac_final_value,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }
