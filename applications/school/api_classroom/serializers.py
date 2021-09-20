from rest_framework import serializers

from applications.school.models import Classroom, SchoolPeriod
from applications.users.models import Student

# TODO: Verificar si el método validate_students() es eficiente


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Curse Leve Validation
    def validate_curse_level(self, value):
        if value == 0 or value > 3:
            raise serializers.ValidationError('Error, no existe este Nivel de Curso.')
        return value

    # School Period Id Validation
    def validate_school_period(self, value):
        if not SchoolPeriod.objects.is_period_active(value.id):
            raise serializers.ValidationError('Error, el Período Lectivo que ingresó no existe o no está activo.')
        return value

    # Validate Students
    def validate_students(self, value):
        if value:
            for student in value:
                if not Student.objects.is_active(student.id):
                    raise serializers.ValidationError(f'Error, este Estudiante [{student}] no existe.')
        return value

    def to_representation(self, instance):
        return dict(
            name=instance.name,
            curse_level=instance.curse_level.__str__(),
            capacity=instance.capacity,
            school_period=dict(
                name=instance.school_period.__str__(),
                period_date=instance.school_period.get_period_date()
            ),
            # students=instance.students
        )
