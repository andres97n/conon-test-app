from django.contrib import admin

from .models import SchoolPeriod, KnowledgeArea, Asignature, \
    Classroom, AsignatureClassroom

admin.site.register(SchoolPeriod)
admin.site.register(KnowledgeArea)
admin.site.register(Asignature)
admin.site.register(Classroom)
admin.site.register(AsignatureClassroom)
