from rest_framework import serializers

from applications.users.models import User
from applications.abp_steps.models import AnswerStepOneAbp, QuestionStepOneAbp


class AnswerStepOneAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerStepOneAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # User Validate
    def validate_user(self, value):
        if not User.objects.type_user_exists(value.id, 1):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario debe ser Estudiante.'
                }
            )
        return value

    # Create Answer ABP
    def create(self, validated_data):
        if not QuestionStepOneAbp.objects.exists_question_abp(
                validated_data['question_step_one_abp'].id
        ):
            raise serializers.ValidationError(
                {
                    'question_step_one_abp': 'Error, la pregunta enviada no existe.'
                }
            )
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario envíado no existe, consulte con el Administrador.'
                }
            )
        answer_abp = AnswerStepOneAbp(**validated_data)
        answer_abp.save()
        return answer_abp

    # Update Answer ABP
    def update(self, instance, validated_data):
        if instance.question_step_one_abp != validated_data['question_step_one_abp']:
            raise serializers.ValidationError(
                {
                    'question_step_one_abp': 'Error, no se puede cambiar de pregunta, '
                                             'consulte con el Administrador.'
                }
            )
        if instance.user != validated_data['user']:
            raise serializers.ValidationError(
                {
                    'user': 'Error, no se puede cambiar de usuario.'
                }
            )
        update_answer_abp = super().update(instance, validated_data)
        update_answer_abp.save()
        return update_answer_abp

    # Answer ABP List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'question_step_one_abp': {
                'id': instance.question_step_one_abp.id,
                'moderator_question': instance.question_step_one_abp.moderator_question
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'teacher_answer': instance.teacher_answer,
            'active': instance.active,
            'created_at': instance.created_at
        }


class AnswersAbpByQuestionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'teacher_answer': instance.teacher_answer,
            'active': instance.active,
            'created_at': instance.created_at
        }


class AnswerAbpByQuestionStepOneAbpSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['answersteponeabp'],
            'question': {
                'id': instance['id']
            },
            'user': {
                'id': ['answersteponeabp__user'],
            },
            'teacher_answer': instance['answersteponeabp__teacher_answer'],
            'active': instance['answersteponeabp__active'],
            'created_at': instance['answersteponeabp__created_at']
        }
