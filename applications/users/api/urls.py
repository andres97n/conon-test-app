from django.urls import path

from applications.users.api.api import user_api_view

url_patterns = [
    path(
        'user/',
        user_api_view,
        name='user_view',
    ),
]
