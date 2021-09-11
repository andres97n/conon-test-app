from django.urls import path

from applications.users.api.api_person.api import person_api_view, person_detail_api_view

urlpatterns = [
    path(
        'person/',
        person_api_view,
        name='person_view',
    ),
    path(
        'person/<int:pk>/',
        person_detail_api_view,
        name='person_detail_view',
    ),
]
