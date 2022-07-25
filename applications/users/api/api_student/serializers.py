from rest_framework import serializers

from applications.users.models import Student, Person
from applications.users.functions import is_person_assigned


# Create or Update Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    """
    person = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        queryset=Person.objects.all()
    )
    """
    user = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Student
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def get_user(self, obj):
        return Student.objects.get_user(obj.id)

    # Validation if the Person exists
    def validate_person(self, value):
        person = Person.objects.is_deleted(value.id)
        if person is None:
            raise serializers.ValidationError('Error, esta Persona no existe.')
        return value

    def validate_emergency_contact(self, value):
        if value:
            if not value.isdecimal():
                raise serializers.ValidationError(
                    'Error, el contacto debe contener solo números.'
                )
            elif len(value) > 10:
                raise serializers.ValidationError(
                    'Error, el número de contacto no debe tener más de 10 números.'
                )
        return value

    # Create Student Method
    def create(self, validated_data):
        if is_person_assigned(validated_data['person'].id):
            raise serializers.ValidationError(
                {
                    'person': ['Error, esta Persona ya fue asignada.']
                }
            )

        student = Student(**validated_data)
        student.save()
        return student

    # Update Student Method
    def update(self, instance, validated_data):
        if instance.person != validated_data['person']:
            raise serializers.ValidationError(
                {
                    'person': ['Error, no se puede cambiar de Persona.']
                }
            )
        update_student = super().update(instance, validated_data)
        update_student.save()
        return update_student

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = None

        if data['user']:
            user = {
                'id': data['user'][0],
                'username': data['user'][1],
                'email': data['user'][2]
            }
        else:
            user = {
                'id': 0,
                'username': 'No existe',
                'email': 'No existe'
            }

        return {
            'id': instance.id,
            'person': {
                'id': instance.person.id,
                'identification_type': instance.person.get_identification_type_display(),
                'identification': instance.person.identification,
                'name': instance.person.name,
                'last_name': instance.person.last_name,
                'gender': instance.person.get_gender_display(),
                'age': instance.person.age,
                'phone': instance.person.phone
            },
            'user': user,
            'representative_name': instance.representative_name,
            'emergency_contact': instance.emergency_contact,
            'expectations': instance.expectations,
            'observations': instance.observations,
            'created_at': instance.created_at
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


class StudentShortListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'person',
        ]

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'identification': instance['person__identification'],
            'name': f"{instance['person__name']} {instance['person__last_name']}",
            'age': instance['person__age'],
            'email': instance['person__user__email']
        }


class StudentListByUserSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'user': instance['person__user__id'],
            'identification': instance['person__identification'],
            'name': f"{instance['person__name']} {instance['person__last_name']}",
            'email': instance['person__user__email']
        }


class StudentObjectShotListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['students'],
            'identification': instance['students__person__identification'],
            'name': f"{instance['students__person__name']} {instance['students__person__last_name']}",
        }


class StudentShorListByConversationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['students'],
            'identification': instance['students__person__identification'],
            'name': f"{instance['students__person__name']} {instance['students__person__last_name']}",
            'user': instance['students__person__user']
        }


class StudentsByNewConversationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['students__person__user'],
            'identification': instance['students__person__identification'],
            'name': f"{instance['students__person__name']} {instance['students__person__last_name']}",
        }
