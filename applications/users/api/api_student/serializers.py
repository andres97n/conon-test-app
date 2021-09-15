from rest_framework import serializers

from applications.users.models import Student, Person

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


# Person List or Person Detail Serializer
class StudentListSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField

    class Meta:
        model = Student
        fields = [
            'id',
            'person',
            'representative_name',
            'emergency_contact',
            'expectations',
        ]

    # Return Person data of the Student
    def get_person(self, obj):
        person = Student.objects.get_person_data()
        return person
