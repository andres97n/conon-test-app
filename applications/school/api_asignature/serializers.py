from rest_framework import serializers

from applications.school.models import Asignature, KnowledgeArea


class AsignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignature
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Validate Knowledge Area
    def validate_knowledge_area(self, value):
        if not KnowledgeArea.objects.is_active(value.id):
            raise serializers.ValidationError('Error, esta Área de Conocimiento no existe.')
        return value

    # Return Asignature Data
    def to_representation(self, instance):
        return dict(
            name=instance.name,
            objective=instance.objective,
            knowledge_area=instance.knowledge_area,
            observations=instance.observations,
            # classrooms = instance.classrooms
        )
