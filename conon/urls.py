"""conon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView

from applications.users.views import LoginView, LogoutView, RefreshView
from applications.users.api.api_user.api import is_username_valid

schema_view = get_schema_view(
   openapi.Info(
      title="CONON API",
      default_version='v0.1',
      description="An educational platform for learn better.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="novilloa21@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('login/', Login.as_view(), name='login'),
    # path('logout/', Logout.as_view(), name='logout'),
    # path('refresh-token/', UserToken.as_view(), name='refresh_token'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth/username/<str:username>/', is_username_valid, name='exists_username'),
    path('token/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/api/', include('applications.users.routers')),
    path('school/api/', include('applications.school.routers')),
    path('topic/api/', include('applications.topic.routers')),
    path('dua/api/', include('applications.dua.routers')),
    path('abp/api/', include('applications.abp.routers')),
    path('ac/api/', include('applications.ac.routers')),
    path('abp-steps/api/', include('applications.abp_steps.routers')),
    path('user/api/path/', include('applications.users.urls')),
    path('topic/api/path/', include('applications.topic.urls')),
    path('dua/api/path/', include('applications.dua.urls')),
    path('abp/api/path/', include('applications.abp.urls')),
    path('ac/api/path/', include('applications.ac.urls')),
    path('abp-steps/api/path/', include('applications.abp_steps.urls')),
]

