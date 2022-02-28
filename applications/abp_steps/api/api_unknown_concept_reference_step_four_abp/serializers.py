
from rest_framework import serializers

from applications.abp_steps.models import (UnknownConceptStepFourAbp,
                                           UnknownConceptReferenceStepFourAbp)
from applications.users.models import User


class UnknownConceptReferenceStepFourAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnknownConceptReferenceStepFourAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Unknown Concept Reference ABP
    def create(self, validated_data):
        if not UnknownConceptStepFourAbp.objects.unknown_concept_exists(
                validated_data['unknown_concept_step_four_abp'].id
        ):
            raise serializers.ValidationError(
                {
                    'unknown_concept_step_four_abp': 'Error, el concepto enviado no existe o '
                                                      'está inactivo, consulte con el Administrador.'
                }
            )
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el siguiente usuario no existe o está inactivo '
                            'consulte con el Administrador.'
                }
            )
        unknown_concept_reference_abp = UnknownConceptReferenceStepFourAbp(**validated_data)
        unknown_concept_reference_abp.save()
        return unknown_concept_reference_abp

    # Update Unknown Concept Reference ABP
    def update(self, instance, validated_data):
        if instance.unknown_concept_step_four_abp != validated_data['unknown_concept_step_four_abp']:
            raise serializers.ValidationError(
                {
                    'unknown_concept_step_four_abp': 'Error, no se puede cambiar de concepto, '
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
        update_unknown_concept_reference_abp = super().update(instance, validated_data)
        update_unknown_concept_reference_abp.save()
        return update_unknown_concept_reference_abp


class UnknownConceptReferenceStepFourAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnknownConceptReferenceStepFourAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'unknown_concept_step_four_abp': {
              'id': instance.unknown_concept_step_four_abp.id,
              'unknown_concept': instance.unknown_concept_step_four_abp.unknown_concept
            },
            'user': {
              'id': instance.user.id,
              'name': instance.user.__str__()
            },
            'url_reference': instance.url_reference,
            'active': instance.active,
            'created_at': instance.created_at
        }


class SmallUnknownConceptReferenceStepFourAbpListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'url_reference': instance.url_reference,
            'active': instance.active,
            'created_at': instance.created_at
        }
