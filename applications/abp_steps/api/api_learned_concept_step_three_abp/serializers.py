from rest_framework import serializers

from applications.abp_steps.models import LearnedConceptStepThreeAbp
from applications.abp.models import TeamAbp


class LearnedConceptStepThreeAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnedConceptStepThreeAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Learned Concept ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el estudiante no pertenece a este grupo, '
                                'consulte con el Administrador.'
                }
            )
        learned_concept_abp = LearnedConceptStepThreeAbp(**validated_data)
        learned_concept_abp.save()
        return learned_concept_abp

    # Update Learned Concept ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, no se puede cambiar de referencia, '
                                'consulte con el administrador.'
                }
            )
        update_learned_concept_abp = super().update(instance, validated_data)
        update_learned_concept_abp.save()
        return update_learned_concept_abp


# Return Learned Concept Data
class LearnedConceptListStepThreeAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearnedConceptStepThreeAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_abp': {
                'id': instance.team_abp.id,
                'step': instance.team_abp.step
            },
            'learned_concept': instance.learned_concept,
            'active': instance.active,
            'created_at': instance.created_at
        }
