
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import TeacherAnswerDescriptionSecretaryAc, TeacherAnswerAc


class TeacherAnswerDescriptionSecretaryAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAnswerDescriptionSecretaryAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Teacher Answer Description Secretary AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        if not TeacherAnswerAc.objects.exists_teacher_answer(validated_data['teacher_answer_ac'].id):
            raise serializers.ValidationError(
                {
                    'teacher_answer_ac': 'Error, la respuesta ingresada no existe o está inactiva; '
                                         'consulte con el Administrador.'
                }
            )
        teacher_answer_description_secretary_ac = TeacherAnswerDescriptionSecretaryAc(**validated_data)
        teacher_answer_description_secretary_ac.save()
        return teacher_answer_description_secretary_ac


class TeacherAnswerDescriptionSecretaryAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAnswerDescriptionSecretaryAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_detail_ac': {
                'id': instance.team_detail_ac.id,
                'role_type': instance.team_detail_ac.role_type
            },
            'teacher_answer_ac': {
                'id': instance.teacher_answer_ac.id,
                'teacher_answer': instance.teacher_answer_ac.teacher_answer
            },
            'teacher_answer_description': instance.teacher_answer_description,
            'active': instance.active,
            'created_at': instance.created_at
        }
