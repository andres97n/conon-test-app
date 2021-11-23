from django.contrib import admin

from .models import SchoolPeriod, KnowledgeArea, Asignature, \
    Classroom, AsignatureClassroom, Glossary, GlossaryDetail

admin.site.register(SchoolPeriod)
admin.site.register(KnowledgeArea)
admin.site.register(Asignature)
admin.site.register(Classroom)
admin.site.register(AsignatureClassroom)
admin.site.register(Glossary)
admin.site.register(GlossaryDetail)
