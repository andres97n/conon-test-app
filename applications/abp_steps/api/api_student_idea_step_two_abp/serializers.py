
from rest_framework import serializers

from applications.abp_steps.models import StudentIdeaStepTwoAbp
from applications.abp.models import TeamDetailAbp


class StudentIdeaStepTwoAbpSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentIdeaStepTwoAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Student Idea ABP
    def create(self, validated_data):
        if not TeamDetailAbp.objects.exists_team_detail_abp(
                validated_data['team_detail_abp'].id
        ):
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, el estudiante no pertenece a este grupo, '
                                       'consulte con el Administrador.'
                }
            )
        student_idea_abp = StudentIdeaStepTwoAbp(**validated_data)
        student_idea_abp.save()
        return student_idea_abp

    # Update Student Idea ABP
    def update(self, instance, validated_data):
        if instance.team_detail_abp != validated_data['team_detail_abp']:
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, no se puede cambiar de referencia, '
                                       'consulte con el administrador.'
                }
            )
        update_student_idea_abp = super().update(instance, validated_data)
        update_student_idea_abp.save()
        return update_student_idea_abp

    # Return Student Idea Abp
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_detail_abp': {
              'id': instance.team_detail_abp.id,
              'user': {
                  'id': instance.team_detail_abp.user.id,
                  'name': instance.team_detail_abp.user.__str__()
              },
            },
            'student_idea': instance.student_idea,
            'active': instance.active,
            'created_at': instance.created_at
        }


class StudentIdeaStepTwoAbpByTeamDetailSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'student_idea': instance.student_idea,
            'active': instance.active,
            'created_at': instance.created_at
        }


class TeamStudentIdeasStepTwoAbpSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['studentideasteptwoabp'],
            'student_idea': instance['studentideasteptwoabp__student_idea'],
            'active': instance['studentideasteptwoabp__active'],
            'created_at': instance['studentideasteptwoabp__created_at']
        }
