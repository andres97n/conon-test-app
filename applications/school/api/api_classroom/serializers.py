from rest_framework import serializers

from applications.school.models import Classroom, SchoolPeriod
from applications.users.models import Student


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Curse Level Validation
    def validate_curse_level(self, value):
        if value == 0 or value > 3:
            raise serializers.ValidationError('Error, no existe este Nivel de Curso.')
        return value

    # Validate Students
    def validate_students(self, value):
        if value:
            for student in value:
                if not Student.objects.is_active(student.id):
                    raise serializers.ValidationError(
                        {
                            'students': 'Error, el siguiente Estudiante no existe.'
                        }
                    )
        return value

    # Create a Classroom
    def create(self, validated_data):
        if not SchoolPeriod.objects.is_period_active(validated_data['school_period'].id):
            raise serializers.ValidationError(
                {
                    'school_period': 'Error, el Período Lectivo que ingresó no existe o no '
                                     'está activo.'
                }
            )
        classroom = Classroom(**validated_data)
        classroom.save()
        return classroom

    # Update Classroom
    def update(self, instance, validated_data):
        if instance.school_period != validated_data['school_period']:
            raise serializers.ValidationError(
                {
                    'school_period': 'Error, una vez ingresado el Período Lectivo no se puede '
                                     'cambiar el mismo.'
                }
            )
        update_classroom = super().update(instance, validated_data)
        update_classroom.save()
        return update_classroom

    # Get Classroom List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'curse_level': instance.curse_level,
            'capacity': instance.capacity,
            'school_period': {
                'id': instance.school_period.id,
                'name': instance.school_period.__str__(),
                'period_date': instance.school_period.get_period_date()
            },
            'state': instance.state,
            'created_at': instance.created_at
        }


class ClassroomShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        include = [
            'id',
            'name',
            'curse_level'
        ]

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'curse_level': instance['curse_level']
        }


class StudentsForManyChoicesSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        read_only=True
    )
    identification = serializers.CharField(
        read_only=True
    )
    name = serializers.CharField(
        read_only=True
    )

    def get_email_by_user(self, pk):
        if pk is None:
            return None
        return Student.objects.get_student_email_by_user_id(pk=pk)

    def to_representation(self, instance):
        result = self.get_email_by_user(instance['students__person__user'])
        if result is None:
            email = None
        else:
            email = result['person__user__email']

        return {
            'id': instance['students'],
            'identification': instance['students__person__identification'],
            'name': f"{instance['students__person__name']} {instance['students__person__last_name']}",
            'age': instance['students__person__age'],
            'email': email
        }


class StudentsByClassroomForGroupsSerializer(serializers.Serializer):

    def get_email_by_user(self, pk):
        if pk is None:
            return None
        return Student.objects.get_student_email_by_user_id(pk=pk)

    def to_representation(self, instance):
        result = self.get_email_by_user(instance['students__person__user'])
        if result is None:
            email = None
        else:
            email = result['person__user__email']
        return {
            'id': instance['students'],
            'user': instance['students__person__user'],
            'identification': instance['students__person__identification'],
            'name': f"{instance['students__person__name']} {instance['students__person__last_name']}",
            'email': email
        }

