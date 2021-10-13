from django.contrib import admin

from .models import SchoolPeriod, KnowledgeArea, Asignature, \
    Classroom, AsignatureClassroom, Glosary, GlosaryDetail

admin.site.register(SchoolPeriod)
admin.site.register(KnowledgeArea)
admin.site.register(Asignature)
admin.site.register(Classroom)
admin.site.register(AsignatureClassroom)
admin.site.register(Glosary)
admin.site.register(GlosaryDetail)
