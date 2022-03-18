from rest_framework import serializers

from applications.abp.models import EvaluationAbp, Abp, TeamDetailAbp


class EvaluationAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationAbp
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

    # Create Evaluation ABP
    def create(self, validated_data):
        if not Abp.objects.abp_exists(validated_data['abp'].id):
            raise serializers.ValidationError(
                {
                    'abp': 'Error, la metodología ABP ingresada no es válida; consulte con el Administrador.'
                }
            )
        if not TeamDetailAbp.objects.exists_team_detail_abp(validated_data['team_detail_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, el Estudiante no existe o está inactivo; consulte '
                                       'con el Administrador.'
                }
            )
        evaluation_abp = EvaluationAbp(**validated_data)
        evaluation_abp.save()
        return evaluation_abp

    # Update Evaluation ABP
    def update(self, instance, validated_data):
        if instance.abp != validated_data['abp']:
            raise serializers.ValidationError(
                {
                    'abp': 'Error, no se puede cambiar de Metodología; por favor consulte '
                           'con el Administrador.'
                }
            )
        if instance.team_detail_abp != validated_data['team_detail_abp']:
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, no se puede cambiar el Estudiante ingresado; '
                                       'consulte con el Administrador.'
                }
            )
        update_evaluation_abp = super().update(instance, validated_data)
        update_evaluation_abp.save()
        return update_evaluation_abp

    # Return Evaluation ABP
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
            'team_detail_abp': {
                'id': instance.team_detail_abp.id,
                'user': {
                    'id': instance.team_detail_abp.user.id,
                    'name': instance.team_detail_abp.user.__str__()
                }
            },
            'description': instance.description,
            'final_grade': instance.final_grade,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }

