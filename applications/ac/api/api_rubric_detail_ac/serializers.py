
from rest_framework import serializers

from applications.ac.models import RubricDetailAc, RubricAc


class RubricDetailAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricDetailAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Rubric Detail AC
    def create(self, validated_data):
        if not RubricAc.objects.exists_rubric_ac(validated_data['rubric_ac'].id):
            raise serializers.ValidationError(
                {
                    'rubric_ac': 'Error, la rúbrica ingresada no es válida; '
                                 'consulte con el Administrador.'
                }
            )
        rubric_detail_ac = RubricDetailAc(**validated_data)
        rubric_detail_ac.save()
        return rubric_detail_ac

    # Update Rubric Detail AC
    def update(self, instance, validated_data):
        if instance.rubric_ac != validated_data['rubric_ac']:
            raise serializers.ValidationError(
                {
                    'rubric_ac': 'Error, no se puede cambiar de pertenencia; '
                                 'por favor consulte con el Administrador.'
                }
            )
        update_rubric_detail_ac = super().update(instance, validated_data)
        update_rubric_detail_ac.save()
        return update_rubric_detail_ac


class RubricDetailAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricDetailAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rubric_ac': {
                'id': instance.rubric_ac.id,
                'description_rubric': instance.rubric_ac.description_rubric,
            },
            'detail_title': instance.detail_title,
            'detail_description': instance.detail_description,
            'percentage_grade': instance.percentage_grade,
            'rating_value': instance.rating_value,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }


class RubricDetailAcShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'detail_title': instance.detail_title,
            'detail_description': instance.detail_description,
            'percentage_grade': instance.percentage_grade,
            'rating_value': instance.rating_value,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }
