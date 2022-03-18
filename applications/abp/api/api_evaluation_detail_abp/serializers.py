from rest_framework import serializers

from applications.abp.models import EvaluationDetailAbp, EvaluationAbp


class EvaluationDetailAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationDetailAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Evaluation Detail ABP
    def create(self, validated_data):
        if not EvaluationAbp.objects.evaluation_abp_exists(validated_data['evaluation_abp'].id):
            raise serializers.ValidationError(
                {
                    'evaluation_abp': 'Error, la evaluación ingresada no es válida; consulte con el Administrador.'
                }
            )
        evaluation_detail_abp = EvaluationDetailAbp(**validated_data)
        evaluation_detail_abp.save()
        return evaluation_detail_abp

    # Update Evaluation Detail ABP
    def update(self, instance, validated_data):
        if instance.evaluation_abp != validated_data['evaluation_abp']:
            raise serializers.ValidationError(
                {
                    'evaluation_abp': 'Error, no se puede cambiar de evaluación; por favor consulte con el '
                                      'Administrador. '
                }
            )
        update_evaluation_detail_abp = super().update(instance, validated_data)
        update_evaluation_detail_abp.save()
        return update_evaluation_detail_abp

    # Return Evaluation Detail ABP
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'evaluation_abp': {
                'id': instance.evaluation_abp.id,
                'description': instance.evaluation_abp.description,
                'abp': instance.evaluation_abp.abp.id,
                'team_detail_abp': {
                    'id': instance.evaluation_abp.team_detail_abp.id,
                    'user': {
                        'id': instance.evaluation_abp.team_detail_abp.user.id,
                        'name': instance.evaluation_abp.team_detail_abp.user.__str__()
                    }
                },
            },
            "title_evaluation_detail": instance.title_evaluation_detail,
            'evaluation_description': instance.evaluation_description,
            'grade_percentage': instance.grade_percentage,
            'rating_value': instance.rating_value,
            'active': instance.active,
            'created_at': instance.created_at
        }


class EvaluationDetailAbpListByEvaluationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            "title_evaluation_detail": instance.title_evaluation_detail,
            'evaluation_description': instance.evaluation_description,
            'grade_percentage': instance.grade_percentage,
            'rating_value': instance.rating_value,
            'active': instance.active,
            'created_at': instance.created_at
        }
