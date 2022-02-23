from rest_framework import serializers

from applications.abp_steps.models import (LearnedConceptReferenceStepThreeAbp,
                                           LearnedConceptStepThreeAbp)
from applications.users.models import User


class LearnedConceptReferenceStepThreeAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnedConceptReferenceStepThreeAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Learned Concept Reference ABP
    def create(self, validated_data):
        if not LearnedConceptStepThreeAbp.objects.learned_concept_exists(
                validated_data['learned_concept_step_three_abp'].id
        ):
            raise serializers.ValidationError(
                {
                    'learned_concept_step_three_abp': 'Error, el siguiente enlace no pertenece a '
                                                      'este concepto, consulte con el Administrador.'
                }
            )
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el siguiente usuario no existe o está inactivo '
                            'consulte con el Administrador.'
                }
            )
        learned_concept_reference_abp = LearnedConceptReferenceStepThreeAbp(**validated_data)
        learned_concept_reference_abp.save()
        return learned_concept_reference_abp

    # Update Learned Concept Reference ABP
    def update(self, instance, validated_data):
        if instance.learned_concept_step_three_abp != validated_data['learned_concept_step_three_abp']:
            raise serializers.ValidationError(
                {
                    'learned_concept_step_three_abp': 'Error, no se puede cambiar de concepto, '
                                                      'consulte con el administrador.'
                }
            )
        if instance.user != validated_data['user']:
            raise serializers.ValidationError(
                {
                    'user': 'Error, no se puede cambiar de usuario, '
                            'consulte con el administrador.'
                }
            )
        update_learned_concept_reference_abp = super().update(instance, validated_data)
        update_learned_concept_reference_abp.save()
        return update_learned_concept_reference_abp


class LearnedConceptReferenceListStepThreeAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearnedConceptReferenceStepThreeAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance,
            'learned_concept_step_three_abp': {
                'id': instance.learned_concept_step_three_abp.id,
                'learned_concept': instance.learned_concept_step_three_abp.learned_concept
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'url_reference': instance.url_reference,
            'active': instance.active,
            'created_at': instance.created_at
        }
