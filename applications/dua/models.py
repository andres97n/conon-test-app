from django.db import models

from applications.base.models import BaseModel
from applications.topic.models import Topic
from applications.users.models import User
from .api.api_dua.managers import DuaManager
from .api.api_activity.managers import ActivityManager
from .api.api_question.managers import QuestionManager
from .api.api_activity_student.managers import ActivityStudentManager
from .api.api_answer.managers import AnswerManager

# TODO: Revisar si la relación de Activity con Topic y foreign o onetoone


class Dua(BaseModel):

    class DuaStatus(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    written_conceptualization = models.TextField(
        null=False,
        blank=False
    )
    oral_conceptualization = models.JSONField(
        null=False,
        blank=False
    )
    example = models.TextField(
        null=False,
        blank=False
    )
    video = models.JSONField(
        null=True,
        blank=True
    )
    images = models.JSONField(
        null=False,
        blank=True
    )
    extra_information = models.URLField(
        null=True,
        blank=True
    )
    observations = models.TextField(
        null=True,
        blank=True
    )
    state = models.PositiveSmallIntegerField(
        'estado',
        choices=DuaStatus.choices,
        default=1,
        null=True,
        blank=True,
    )

    topic = models.OneToOneField(
        Topic,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = DuaManager()

    class Meta:
        db_table = 'dua'
        verbose_name = 'DUA'

    def __str__(self):
        return self.topic.title


class Activity(BaseModel):
    description = models.TextField(
        null=False,
        blank=False
    )
    objective = models.TextField(
        null=True,
        blank=True
    )
    final_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=10,
        null=False,
        blank=False
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = ActivityManager()

    class Meta:
        db_table = 'activity'
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.description


class Question(BaseModel):
    title = models.TextField(
        null=False,
        blank=False
    )
    '''
    {
    answer_1={
            'literal': 'A',
            'detail': '',
            'value': '0,2'
        }
    }
    '''
    answers = models.JSONField(
        default=dict,
        null=False,
        blank=False
    )
    value = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        default=0,
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=True,
        blank=True
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = QuestionManager()

    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title


class ActivityStudent(BaseModel):
    qualification = models.FloatField(
        null=False,
        blank=False
    )
    observation = models.TextField(
        null=True,
        blank=True
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = ActivityStudentManager()

    class Meta:
        db_table = 'activity_student'
        verbose_name = 'Activity Student'
        verbose_name_plural = 'Activities Student'

    def __str__(self):
        return self.activity.description

    def get_qualification(self):
        return self.qualification


class Answer(BaseModel):
    """
    {
        'literal': 'A',
        'detail': '',
        'value': '0,2'
    }
    """
    detail = models.JSONField(
        default=dict,
        null=False,
        blank=False
    )
    value = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        null=False,
        blank=False
    )

    activity_student = models.ForeignKey(
        ActivityStudent,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    objects = AnswerManager()

    class Meta:
        db_table = 'answer'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.value

    def get_detail(self):
        return self.detail
