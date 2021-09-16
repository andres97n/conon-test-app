from rest_framework import serializers

from applications.users.models import Teacher, Person
from applications.users.functions import is_person_assigned


# Create or Update Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(
        write_only=True,
        many=False,
        queryset=Person.objects.all()
    )

    class Meta:
        model = Teacher
        fields = [
            'person',
            'title',
            'objective',
        ]

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
        teacher = Teacher.objects.get_teacher_person(obj.id)
        if teacher is not None:
            return dict(
                identification=teacher['person__identification'],
                name=teacher['person__name'],
                last_name=teacher['person__last_name'],
                age=teacher['person__age'],
                phone=teacher['person__phone'],
            )
        return teacher
