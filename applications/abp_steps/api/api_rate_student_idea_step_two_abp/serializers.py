
from rest_framework import serializers
from applications.abp_steps.models import RateStudentIdeaStepTwoAbp, StudentIdeaStepTwoAbp
from applications.users.models import User


class RateStudentIdeaStepTwoAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateStudentIdeaStepTwoAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Rate Student Idea ABP
    def create(self, validated_data):
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario enviado no existe, consulte con el Administrador.'
                }
            )
        if not StudentIdeaStepTwoAbp.objects.exists_student_idea(
                validated_data['student_idea_step_two_abp'].id
        ):
            raise serializers.ValidationError(
                {
                    'student_idea_step_two_abp': 'Error, la idea enviada no existe, '
                                                 'consulte con el Administrador.'
                }
            )
        rate_student_idea_abp = RateStudentIdeaStepTwoAbp(**validated_data)
        rate_student_idea_abp.save()
        return rate_student_idea_abp

    # Update Rate Student Idea ABP
    def update(self, instance, validated_data):
        if instance.user != validated_data['user']:
            raise serializers.ValidationError(
                {
                    'user': 'Error, no se puede cambiar de Usuario, consulte con el administrador.'
                }
            )
        if instance.student_idea_step_two_abp != validated_data['student_idea_step_two_abp']:
            raise serializers.ValidationError(
                {
                    'student_idea_step_two_abp': 'Error, no se puede cambiar de Idea, '
                                                 'consulte con el administrador.'
                }
            )
        update_rate_student_idea_abp = super().update(instance, validated_data)
        update_rate_student_idea_abp.save()
        return update_rate_student_idea_abp


# Return Rate Student Idea Data
class RateStudentIdeaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateStudentIdeaStepTwoAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'student_idea_step_two_abp': {
                'id': instance.student_idea_step_two_abp.id,
                'student_idea': instance.student_idea_step_two_abp.student_idea
            },
            'rate_student_idea': instance.rate_student_idea,
            'active': instance.active,
            'created_at': instance.created_at
        }


class RateStudentIdeaByIdeaSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'rate_student_idea': instance.rate_student_idea,
            'active': instance.active,
            'created_at': instance.created_at
        }
