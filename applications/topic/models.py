from django.db import models

from applications.base.models import BaseModel
from applications.users.models import Student, User
from applications.school.models import Classroom, Asignature
from applications.topic.api.api_topic.managers import TopicManager
from applications.topic.api.api_comment.managers import CommentManager
from applications.topic.api.api_reply.managers import ReplyManager

# TODO: Revisar porque en algunos raise errors en serializers se muestra como array y en otros no


class Topic(BaseModel):
    class MethodologiesChoices(models.IntegerChoices):
        DUA = 1
        ABP = 2
        AC = 3

    title = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )
    description = models.TextField(
        null=False,
        blank=False
    )
    objective = models.TextField(
        null=False,
        blank=False
    )
    type = models.PositiveSmallIntegerField(
        choices=MethodologiesChoices.choices,
        null=False,
        blank=False
    )
    start_at = models.DateTimeField(
        null=False,
        blank=False
    )
    end_at = models.DateTimeField(
        null=False,
        blank=False
    )
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )
    observations = models.TextField(
        default='S/N',
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    asignature = models.ForeignKey(
        Asignature,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    students = models.ManyToManyField(
        Student,
        blank=True
    )

    objects = TopicManager()

    class Meta:
        db_table = 'topic'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.title


class Comment(BaseModel):
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )
    detail = models.TextField(
        null=False,
        blank=False
    )
    end_at = models.DateTimeField(
        null=True,
        blank=True
    )
    wrong_use = models.BooleanField(
        default=False,
        null=False,
        blank=True
    )
    state = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    topic = models.ForeignKey(
        Topic,
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

    objects = CommentManager()

    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.title

    def get_detail(self):
        return self.detail


class Reply(BaseModel):

    detail = models.TextField(
        null=False,
        blank=False
    )
    wrong_use = models.BooleanField(
        default=False,
        null=False,
        blank=True
    )
    state = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    comment = models.ForeignKey(
        Comment,
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

    objects = ReplyManager()

    class Meta:
        db_table = 'reply'
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.detail
