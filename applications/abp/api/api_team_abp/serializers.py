from rest_framework import serializers
from applications.abp.models import TeamAbp, Abp
from applications.users.models import Student


class TeamAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # State Validation
    def validate_state(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no existe este Nivel de Curso.'
                }
            )
        return value

    # Create Team ABP
    def create(self, validated_data):
        if not Abp.objects.abp_exists(validated_data['abp'].id):
            raise serializers.ValidationError(
                {
                    'abp': 'Error, la metodología ABP ingresada no es válida; '
                           'consulte con el Administrador.'
                }
            )
        team_abp = TeamAbp(**validated_data)
        team_abp.save()
        return team_abp

    # Update Team ABP
    def update(self, instance, validated_data):
        if instance.abp != validated_data['abp']:
            raise serializers.ValidationError(
                {
                    'abp': 'Error, no se puede cambiar de pertenencia; por favor '
                           'consulte con el Administrador.'
                }
            )
        update_team_abp = super().update(instance, validated_data)
        update_team_abp.save()
        return update_team_abp

    # Return Team ABP
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'abp': {
                'id': instance.abp.id,
                'problem': instance.abp.problem,
                'topic': {
                    'id': instance.abp.topic.id,
                    'title': instance.abp.topic.title
                },
            },
            'step': instance.get_step_display(),
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }


class StudentsInTeamAbpSerializer(serializers.Serializer):
    def to_representation(self, instance):
        student = Student.objects.get_student_by_user_object(instance['teamdetailabp__user_id'])
        if student is None:
            student = 'Sin nombre'
        else:
            student = student.__str__()
        return {
            'id': instance['id'],
            'step': instance['step'],
            'team_detail_abp': instance['teamdetailabp__id'],
            'user': {
                'id': instance['teamdetailabp__user_id'],
                'name': student
            },
            'is_moderator': instance['teamdetailabp__is_moderator'],
            'active': instance['teamdetailabp__active']
        }


class TeamAbpShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'step': instance.step,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }
