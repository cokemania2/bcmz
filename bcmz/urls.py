from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from account.api.views import UserViewSet, TokenViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'token', TokenViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
