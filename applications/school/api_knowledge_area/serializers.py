from rest_framework import serializers

from applications.school.models import KnowledgeArea
from applications.users.models import Teacher


# TODO: Investigar la manera de retornar los datos de los
#   profesores dentro de la lista del área


class KnowledgeAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgeArea
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Validate Teachers
    def validate_teachers(self, value):
        if value:
            for teacher in value:
                if not Teacher.objects.is_active(teacher.id):
                    raise serializers.ValidationError(f'Error, este Docente [{teacher}] no existe.')
        return value

    def validate(self, attrs):
        if attrs['coordinator'].id == attrs['sub_coordinator'].id:
            raise serializers.ValidationError('Error, el Coordinador no puede ser el mismo que el Sub coordinador.')

        return attrs

    def to_representation(self, instance):

        return dict(
            id=instance.id,
            name=instance.name,
            coordinator=dict(
                name=instance.coordinator.person.name,
                last_name=instance.coordinator.person.last_name
            ),
            sub_coordinator=dict(
                name=instance.sub_coordinator.person.name,
                last_name=instance.sub_coordinator.person.last_name
            ),
            objective=instance.objective,
            # teachers=instance.teachers
        )
