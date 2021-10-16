from rest_framework import serializers

from applications.school.models import Classroom, SchoolPeriod
from applications.users.models import Student
from applications.users.api.api_student.serializers import StudentListManyToMany


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Curse Leve Validation
    def validate_curse_level(self, value):
        if value == 0 or value > 3:
            raise serializers.ValidationError('Error, no existe este Nivel de Curso.')
        return value

    # Validate Students
    def validate_students(self, value):
        if value:
            for student in value:
                if not Student.objects.is_active(student.id):
                    raise serializers.ValidationError(f'Error, el siguiente Estudiante no existe.')
        return value

    def get_students(self, students=None):
        student_serializer = StudentListManyToMany(students, many=True)
        return student_serializer.data

    # Create a Classroom
    def create(self, validated_data):
        if not SchoolPeriod.objects.is_period_active(validated_data['school_period'].id):
            raise serializers.ValidationError('Error, el Período Lectivo que ingresó no existe o no está activo.')
        classroom = Classroom(**validated_data)
        classroom.save()
        return classroom

    # Update Classroom
    def update(self, instance, validated_data):
        if instance.school_period != validated_data['school_period']:
            raise serializers.ValidationError('Error, una vez ingresado el Período Lectivo no se puede cambiar el mismo.')
        update_classroom = super().update(instance, validated_data)
        update_classroom.save()
        return update_classroom

    # Get Classroom List
    def to_representation(self, instance):
        return {
            'name': instance.name,
            'curse_level': instance.curse_level,
            'capacity': instance.capacity,
            'school_period': {
                'name': instance.school_period.__str__(),
                'period_date': instance.school_period.get_period_date()
            },
            'students': self.get_students(instance.students),
            'created_at': instance.created_at
        }
