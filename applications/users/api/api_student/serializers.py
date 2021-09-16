from rest_framework import serializers

from applications.users.models import Student, Person
from applications.users.functions import is_person_assigned


# TODO: Validar los números de teléfono


# Create or Update Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        queryset=Person.objects.all()
    )

    class Meta:
        model = Student
        fields = [
            'person',
            'representative_name',
            'emergency_contact',
            'expectations',
            'observations'
        ]

    # Create Student Method
    def create(self, validated_data):
        if is_person_assigned(validated_data['person'].id):
            raise serializers.ValidationError('Error, esta Persona ya fue asignada.')

        student = Student(**validated_data)
        student.save()
        return student

    # Update Student Method
    def update(self, instance, validated_data):
        if instance.person != validated_data['person']:
            raise serializers.ValidationError('Error, no se puede cambiar de Persona.')
        update_student = super().update(instance, validated_data)
        update_student.save()
        return update_student


# Person List or Person Detail Serializer
class StudentListSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'person',
            'representative_name',
            'emergency_contact',
            'expectations',
            'observations'
        ]

    # Return Person data of the Student
    def get_person(self, obj):
        student = Student.objects.get_person_data(pk=obj.id)
        if student is not None:
            return dict(
                identification=student['person__identification'],
                name=student['person__name'],
                last_name=student['person__last_name'],
                gender=student['person__gender'],
                phone=student['person__phone'],
            )
        return person
