from rest_framework import serializers

from applications.abp.models import RubricAbp, Abp


class RubricAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # State Validation
    def validate_state(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no existe este estado.'
                }
            )
        return value

    # Create Rubric ABP
    def create(self, validated_data):
        if not Abp.objects.abp_exists(validated_data['abp'].id):
            raise serializers.ValidationError(
                {
                    'abp': 'Error, la metodología ABP ingresada no es válida; consulte con el Administrador.'
                }
            )
        rubric_abp = RubricAbp(**validated_data)
        rubric_abp.save()
        return rubric_abp

    # Update Rubric ABP
    def update(self, instance, validated_data):
        if instance.abp != validated_data['abp']:
            raise serializers.ValidationError(
                {
                    'abp': 'Error, no se puede cambiar de pertenencia; por favor consulte con el Administrador.'
                }
            )
        update_rubric_abp = super().update(instance, validated_data)
        update_rubric_abp.save()
        return update_rubric_abp

    # Return Rubric ABP
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'abp': {
                'id': instance.abp.id,
                'problem': instance.abp.problem,
                'topic': {
                    'id': instance.abp.topic.id,
                    'title': instance.abp.topic.title
                },
            },
            'description_rubric': instance.description_rubric,
            'abp_final_value': instance.abp_final_value,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }


class RubricDetailSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'abp_final_value': instance['abp_final_value'],
            'rubric_detail_abp': {
                'id': instance['rubricdetailabp'],
                'title': instance['rubricdetailabp__title_detail'],
                'description': instance['rubricdetailabp__description_detail'],
                'grade_percentage': instance['rubricdetailabp__grade_percentage'],
                'rating_value': instance['rubricdetailabp__rating_value'],
                'active': instance['rubricdetailabp__active']
            }
        }


class RubricAbpShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'description_rubric': instance.description_rubric,
            'abp_final_value': instance.abp_final_value,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }
