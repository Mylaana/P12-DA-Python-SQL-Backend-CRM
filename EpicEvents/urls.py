"""
URL configuration for EpicEvents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .authentication import CustomObtainAuthToken, LogoutView
from Client.views import ClientViewSet
from UserProfile.views import UserProfileViewSet, TeamViewSet
from Contract.views import ContractViewSet
from Event.views import EventViewSet


router = DefaultRouter()
router.register('client', ClientViewSet)
router.register('user', UserProfileViewSet)
router.register('team', TeamViewSet)
router.register('contract', ContractViewSet)
router.register('event', EventViewSet)



def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', CustomObtainAuthToken.as_view(), name='token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('sentry-debug/', trigger_error),
]
