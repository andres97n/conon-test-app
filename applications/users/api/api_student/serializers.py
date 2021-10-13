from rest_framework import serializers

from applications.users.models import Student, Person
from applications.users.functions import is_person_assigned

# TODO: Validar los números de teléfono


# Create or Update Student Serializer
class StudentSerializer(serializers.ModelSerializer):

    """
    person = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        queryset=Person.objects.all()
    )
    """

    class Meta:
        model = Student
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validation if the Person exists
    def validate_person(self, value):
        person = Person.objects.is_deleted(value.id)
        if person is None:
            raise serializers.ValidationError('Error, esta Persona no existe.')
        return value

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

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'person': {
                'id': instance.person.id,
                'identification': instance.person.identification,
                'name': instance.person.name,
                'last_name': instance.person.last_name,
             },
            'representative_name': instance.representative_name,
            'emergency_contact': instance.emergency_contact,
            'expectations': instance.expectations,
            'observations': instance.observations
        }

'''
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
                identification=student.person.identification,
                name=student.person.name,
                last_name=student.person.last_name,
                gender=student.person.gender,
                phone=student.person.phone,
            )
        return student
'''


class StudentListByClassroom(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'person',
        ]

    def to_representation(self, instance):
        return dict(
            id=instance.id,
            identification=instance.person.identification,
            name=instance.__str__()
        )

