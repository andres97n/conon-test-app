from rest_framework import serializers

from applications.abp.models import RubricDetailAbp, RubricAbp


class RubricDetailAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricDetailAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Rubric Detail ABP
    def create(self, validated_data):
        if not RubricAbp.objects.rubric_exists(validated_data['rubric_abp'].id):
            raise serializers.ValidationError(
                {
                    'rubric_abp': 'Error, la rúbrica ingresada no es válida; '
                                  'consulte con el Administrador.'
                }
            )
        rubric_detail_abp = RubricDetailAbp(**validated_data)
        rubric_detail_abp.save()
        return rubric_detail_abp

    # Update Rubric Detail ABP
    def update(self, instance, validated_data):
        if instance.rubric_abp != validated_data['rubric_abp']:
            raise serializers.ValidationError(
                {
                    'rubric_abp': 'Error, no se puede cambiar de rúbrica; '
                                  'por favor consulte con el Administrador.'
                }
            )
        update_rubric_detail_abp = super().update(instance, validated_data)
        update_rubric_detail_abp.save()
        return update_rubric_detail_abp

    # Return Rubric Detail ABP
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rubric_abp': {
                'id': instance.rubric_abp.id,
                'description_rubric': instance.rubric_abp.description_rubric,
                'abp': {
                    'id': instance.rubric_abp.abp.id,
                    'problem': instance.rubric_abp.abp.problem
                },
            },
            'title_detail': instance.title_detail,
            'grade_percentage': instance.grade_percentage,
            'rating_value': instance.rating_value,
            'observations_detail': instance.observations_detail,
            'active': instance.active,
            'created_at': instance.created_at
        }

