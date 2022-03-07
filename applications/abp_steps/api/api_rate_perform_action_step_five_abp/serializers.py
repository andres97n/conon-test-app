from rest_framework import serializers

from applications.abp_steps.models import RatePerformActionStepFiveAbp


class RatePerformActionStepFiveAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatePerformActionStepFiveAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Update Rate Perform Action ABP
    def update(self, instance, validated_data):
        if instance.perform_action_step_five_abp != validated_data['perform_action_step_five_abp']:
            raise serializers.ValidationError(
                {
                    'perform_action_step_five_abp': 'Error, no se puede cambiar de referencia, '
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
        update_rate_perform_action_abp = super().update(instance, validated_data)
        update_rate_perform_action_abp.save()
        return update_rate_perform_action_abp


class RatePerformActionStepFiveAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatePerformActionStepFiveAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'perform_action_step_five_abp': {
                'id': instance.perform_action_step_five_abp.id,
                'action': instance.perform_action_step_five_abp.action
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'rate_perform_action': instance.rate_perform_action,
            'active': instance.active,
            'created_at': instance.created_at
        }


class RatePerformActionStepFiveAbpByActionListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'rate_perform_action': instance.rate_perform_action,
            'active': instance.active,
            'created_at': instance.created_at
        }
