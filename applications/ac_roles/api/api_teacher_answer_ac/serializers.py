
from rest_framework import serializers

from applications.users.models import Teacher
from applications.ac_roles.models import TeacherAnswerAc, SpokesmanQuestionAc


class TeacherAnswerAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAnswerAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Teacher Answer AC
    def create(self, validated_data):
        if not Teacher.objects.is_active(validated_data['teacher'].id):
            raise serializers.ValidationError(
                {
                    'teacher': 'Error, el docente ingresado sobre no existe o está inactivo; '
                               'consulte con el Administrador.'
                }
            )
        if not SpokesmanQuestionAc.objects.exists_spokesman_question_ac(validated_data['spokesman_question_ac'].id):
            raise serializers.ValidationError(
                {
                    'spokesman_question_ac': 'Error, la pregunta ingresada no existe o está inactiva; '
                                             'consulte con el Administrador.'
                }
            )
        teacher_answer_ac = TeacherAnswerAc(**validated_data)
        teacher_answer_ac.save()
        return teacher_answer_ac


class TeacherAnswerAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAnswerAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'teacher': {
                'id': instance.teacher.id,
                'name': instance.teacher.__str__()
            },
            'spokesman_question_ac': {
                'id': instance.spokesman_question_ac.id,
                'spokesman_question': instance.spokesman_question_ac.spokesman_question
            },
            'teacher_answer': instance.teacher_answer,
            'active': instance.active,
            'created_at': instance.created_at
        }

