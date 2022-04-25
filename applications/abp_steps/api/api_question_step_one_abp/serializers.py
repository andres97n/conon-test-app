from rest_framework import serializers

from applications.abp_steps.models import QuestionStepOneAbp
from applications.abp.models import TeamAbp

# TODO: Validar que el usuario sea moderador


class QuestionStepOneAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionStepOneAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Question ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el grupo enviado no existe, consulte con el Administrador.'
                }
            )
        question_abp = QuestionStepOneAbp(**validated_data)
        question_abp.save()
        return question_abp

    # Update Question ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, no se puede cambiar de equipo, consulte con el administrador.'
                }
            )
        update_question_abp = super().update(instance, validated_data)
        update_question_abp.save()
        return update_question_abp

    # Question ABP List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_abp': {
                'id': instance.team_abp.id,
                'state': instance.team_abp.get_state_display()
            },
            'moderator_question': instance.moderator_question,
            'active': instance.active,
            'created_at': instance.created_at
        }


class QuestionsByTeamAbpSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['questionsteponeabp'],
            'moderator_question': instance['questionsteponeabp__moderator_question'],
            'active': instance['questionsteponeabp__active'],
            'created_at': instance['questionsteponeabp__created_at']
        }


class QuestionsAbpByTeamAbpSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'moderator_question': instance.moderator_question,
            'active': instance.active,
            'created_at': instance.created_at
        }
