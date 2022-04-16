
from rest_framework import serializers

from applications.ac.models import StudentEvaluationDetailAc, StudentEvaluationAc, RubricDetailAc


class StudentEvaluationDetailAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvaluationDetailAc
        exclude = [
            'updated_at',
            'created_at'
        ]

    # Create Student Evaluation Detail AC
    def create(self, validated_data):
        if not RubricDetailAc.objects.exists_rubric_detail_ac(validated_data['rubric_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'rubric_detail_ac': 'Error, el detalle ingresado sobre la rúbric no es válido; '
                                        'consulte con el Administrador.'
                }
            )
        if not StudentEvaluationAc.objects.exists_student_evaluation_ac(
                validated_data['student_evaluation_ac'].id
        ):
            raise serializers.ValidationError(
                {
                    'student_evaluation_ac': 'Error, la evaluación ingresada no es válida; '
                                          'consulte con el Administrador.'
                }
            )
        student_activity_detail_ac = StudentEvaluationDetailAc(**validated_data)
        student_activity_detail_ac.save()
        return student_activity_detail_ac


class StudentEvaluationDetailAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvaluationDetailAc
        exclude = [
            'updated_at',
            'created_at'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rubric_detail_ac': {
                'id': instance.rubric_detail_ac.id,
                'detail_title': instance.rubric_detail_ac.detail_title
            },
            'student_evaluation_ac': {
                'id': instance.student_evaluation_ac.id,
                'evaluation_type': instance.student_evaluation_ac.evaluation_type
            },
            'evaluation_type': instance.evaluation_type,
            'detail_value': instance.detail_value,
            'detail_body': instance.detail_body,
            'active': instance.active,
            'created_at': instance.created_at
        }


class StudentEvaluationDetailAcShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rubric_detail_ac': instance.rubric_detail_ac.id,
            'evaluation_type': instance.evaluation_type,
            'detail_value': instance.detail_value,
            'detail_body': instance.detail_body,
            'active': instance.active,
            'created_at': instance.created_at
        }
