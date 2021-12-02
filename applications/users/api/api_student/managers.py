from django.db import models


class StudentManager(models.Manager):

    def get_representative(self):
        return f'{self.representative_name} - {self.emergency_contact}'

    def mapper(self):
        return dict(
            id=self.id,
            name=self.person.name,
            last_name=self.person.last_name,
            identification=self.person.identification,
            expectations=self.expectations,
            phone=self.person.phone,
            representative=self.get_representative()
        )

    # Get Person data to a Student
    def get_student_detail_data(self, pk=None):
        student = None
        try:
            student = self.select_related('person').filter(id=pk, auth_state='A').first()
        except:
            pass

        return student

    # Get Student List
    def get_student_list(self):
        students = self.select_related('person').filter(auth_state='A').order_by('person__last_name')
        return students

    def is_active(self, pk=None):
        student = None
        try:
            student = self.filter(id=pk, auth_state='A').first()
        except:
            pass
        if student is None:
            return False

        return True

    def get_user(self, pk=None):
        try:
            return self.filter(person__user__type=2, auth_state='A'). \
                values_list(
                'person__user__id', 'person__user__username', 'person__user__email',
            ).get(id=pk)
        except:
            return None

    def get_many_students(self, students=None):
        result = None
        try:
            if students is not None:
                result = list(self.in_bulk(students).values())
        except:
            pass
        return result

    def get_student_short_data(self, age=None):
        try:
            if age is None:
                return self.select_related('person').filter(person__age=15, auth_state='A').values(
                    'id',
                    'person__identification',
                    'person__name',
                    'person__last_name',
                    'person__user__email',
                    'person__age'
                ).order_by('person__last_name', 'person__identification')
            else:
                return self.select_related('person').filter(person__age=age, auth_state='A').values(
                    'id',
                    'person__identification',
                    'person__name',
                    'person__last_name',
                    'person__user__email',
                    'person__age'
                ).order_by('person__last_name', 'person__identification')
        except:
            return None

    def get_student_email_by_user_id(self, pk=None):
        try:
            return self.select_related('person').filter(person__user=pk, auth_state='A').values(
                'person__user__email'
            ).first()
        except:
            return None
