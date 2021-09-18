from rest_framework import serializers

from applications.users.models import Teacher, Person
from applications.users.functions import is_person_assigned


# Create or Update Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Validation if the Person exists
    def validate_person(self, value):
        person = Person.objects.is_deleted(value.id)
        if person is None:
            raise serializers.ValidationError('Error, esta Persona no existe.')
        return value

    # Create Teacher Method
    def create(self, validated_data):
        if is_person_assigned(validated_data['person'].id):
            raise serializers.ValidationError('Error, esta Persona ya fue asignada.')

        teacher = Teacher(**validated_data)
        teacher.save()
        return teacher

    # Update Teacher Method
    def update(self, instance, validated_data):
        if instance.person != validated_data['person']:
            raise serializers.ValidationError('Error, no se puede cambiar de Persona.')
        update_teacher = super().update(instance, validated_data)
        update_teacher.save()
        return update_teacher

    def to_representation(self, instance):
        return dict(
            id=instance.id,
            person=dict(
                identification=instance.person.identification,
                name=instance.person.name,
                last_name=instance.person.last_name,
            ),
            title=instance.title,
            objective=instance.objective,
        )


# Teacher List or Teacher Detail Serializer
class TeacherListSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'id',
            'person',
            'title',
            'objective'
        ]

    # Return Person Data
    def get_person(self, obj):
        teacher = Teacher.objects.get_person_data(pk=obj.id)
        if teacher is not None:
            return dict(
                identification=teacher.person.identification,
                name=teacher.person.name,
                last_name=teacher.person.last_name,
                age=teacher.person.age,
                phone=teacher.person.phone,
            )
        return teacher
