"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import rest_framework
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
    )
from .api.views import index_view, MessageViewSet,PostViewSet,CommentViewSet,ModsView, UserViewSet

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('post', PostViewSet, basename='post')
router.register('comment', CommentViewSet,basename='comment')
router.register('users',UserViewSet,basename='users')

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mods/',ModsView.as_view(),name='mods'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
