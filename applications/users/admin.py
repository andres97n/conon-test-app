from django.contrib import admin

from .models import Person, User, Teacher, Student, \
    Conversation, Conversation_Detail

# Register your models here.
admin.site.register(Person)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Conversation)
admin.site.register(Conversation_Detail)
