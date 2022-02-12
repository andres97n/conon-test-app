from rest_framework import serializers

from applications.abp_steps.models import InteractionStepOneAbp, OpinionStepOneAbp
from applications.users.models import User


class InteractionStepOneAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = InteractionStepOneAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # User Validate
    def validate_user(self, value):
        if not User.objects.type_user_exists(value.id, 2):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario debe ser Estudiante.'
                }
            )
        return value

    # Create Interaction ABP
    def create(self, validated_data):
        if OpinionStepOneAbp.objects.exists_opinion_abp(validated_data['opinion_step_one_abp'].id):
            raise serializers.ValidationError(
                {
                    'opinion_step_one_abp': 'Error, la opinión a la que hace referencia no existe.'
                }
            )
        if User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario envíado no existe, consulte con el Administrador.'
                }
            )
        interaction_abp = InteractionStepOneAbp(**validated_data)
        interaction_abp.save()
        return interaction_abp

    # Update Interaction ABP
    def update(self, instance, validated_data):
        if instance.opinion_step_one_abp != validated_data['opinion_step_one_abp']:
            raise serializers.ValidationError(
                {
                    'opinion_step_one_abp': 'Error, no se puede cambiar de referencia '
                                            'acerca de la opinión.'
                }
            )
        if instance.user != validated_data['user']:
            raise serializers.ValidationError(
                {
                    'user': 'Error, no se puede cambiar de usuario.'
                }
            )
        update_interaction_abp = super().update(instance, validated_data)
        update_interaction_abp.save()
        return update_interaction_abp

    # Interaction ABP List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'opinion_step_one_abp': {
                'id': instance.opinion_step_one_abp.id,
                'opinion': instance.opinion_step_one_abp.opinion
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'opinion_interaction': instance.get_opinion_interaction_display(),
            'active': instance.active,
            'created_at': instance.created_at
        }


class InteractionStepOneByOpinionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        user_name = User.objects.get_name_by_user_id(instance['interactionsteponeabp__user'])
        return {
            'id': instance['interactionsteponeabp'],
            'user': {
                'id': instance['interactionsteponeabp__user'],
                'name': user_name if user_name else 'Sin nombre'
            },
            'opinion_interaction': instance['interactionsteponeabp__opinion_interaction'],
            'active': instance['interactionsteponeabp__active'],
            'created_at': instance['interactionsteponeabp__created_at']
        }