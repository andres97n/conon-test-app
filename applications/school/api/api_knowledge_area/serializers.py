from rest_framework import serializers

from applications.school.models import KnowledgeArea
from applications.users.models import Teacher


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    """
    teachers_data = serializers.HyperlinkedRelatedField(
        view_name='teachers-by-area',
        read_only=True,
        lookup_field='pk',
        lookup_url_kwarg='pk'
    )
    """

    class Meta:
        model = KnowledgeArea
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validate Area Type
    def validate_type(self, value):
        if value:
            if KnowledgeArea.objects.is_type_exits(type=value):
                raise serializers.ValidationError(
                    {
                        'type': ['Error, es tipo de área ya fue seleccionada.']
                    }
                )
        return value

    # Validate Teachers
    def validate_teachers(self, value):
        if value:
            for teacher in value:
                if not Teacher.objects.is_active(teacher.id):
                    raise serializers.ValidationError(
                        {
                            'teachers': f'Error, este Docente [{teacher}] no existe.'
                        }
                    )
        return value

    def validate(self, attrs):
        if attrs['coordinator'].id == attrs['sub_coordinator'].id:
            raise serializers.ValidationError(
                {
                    'coordinator': 'Error, el Coordinador no puede ser el mismo que el Sub coordinador.'
                }
            )

        return attrs

    # Create a Knowledge Area
    def create(self, validated_data):
        if KnowledgeArea.objects.is_name_exists(validated_data['name']):
            raise serializers.ValidationError(
                {
                    'name': 'Error, esta Área de Conocimiento ya existe.'
                }
            )
        knowledge_area = KnowledgeArea(**validated_data)
        knowledge_area.save()
        return knowledge_area

    # Update Knowledge Area
    def update(self, instance, validated_data):
        if instance.name != validated_data['name']:
            if not KnowledgeArea.objects.is_name_exists(validated_data['name']):
                raise serializers.ValidationError(
                    {
                        'name': 'Error, no se puede cambiar de Área de Conocimiento.'
                    }
                )
        if instance.type != validated_data['type']:
            raise serializers.ValidationError(
                {
                    'type': ['Error, no se puede cambiar el tipo de área.']
                }
            )
        if validated_data['teachers']:
            raise serializers.ValidationError(
                {
                    'teachers': 'Error, no se pueden actualizar los datos de los Docentes.'
                }
            )
        update_knowledge_area = super().update(instance, validated_data)
        update_knowledge_area.save()
        return update_knowledge_area

    # Get Knowledge Area Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'coordinator': {
                'id': instance.coordinator.person.id,
                'name': instance.coordinator.person.full_name()
            },
            'sub_coordinator': {
                'id': instance.sub_coordinator.person.id,
                'name': instance.sub_coordinator.person.full_name()
            },
            'objective': instance.objective,
            'type': instance.type,
            'observations': instance.observations,
            'created_at': instance.created_at
        }


class KnowledgeAreaByAsignature(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        fields = [
            'id',
            'name'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name
        }


class KnowledgeAreaTeachersSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        read_only=True
    )
    teacher_id = serializers.IntegerField(
        read_only=True
    )
    identification = serializers.CharField(
        read_only=True
    )
    name = serializers.CharField(
        read_only=True
    )
    last_name = serializers.CharField(
        read_only=True
    )
    title = serializers.CharField(
        read_only=True
    )

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'teacher_id': instance['teachers__id'],
            'identification': instance['teachers__person__identification'],
            'name': instance['teachers__person__name'],
            'last_name': instance['teachers__person__last_name'],
            'title': instance['teachers__title'],
        }


class TeacherByAreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'person',
            'title',
        ]

    def to_representation(self, instance):
        return {
            'id': instance['teachers'],
            'identification': instance['teachers__person__identification'],
            'name': f"{instance['teachers__person__name']} {instance['teachers__person__last_name']}",
            'title': instance['teachers__title'],
        }

