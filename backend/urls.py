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
from .api.views import *
import djoser

router = routers.DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('comment', CommentViewSet,basename='comment')
router.register('users',UserViewSet,basename='users')
router.register('action',ActionViewSet,basename='actions')
router.register('template',TemplateViewSet,basename='template')
router.register('follow',FollowViewSet,basename='follow')
router.register('meme',MemeContentViewSet,basename='meme')
router.register('statistics',StatisticsViewSet,basename='statistics')
router.register('template',TemplateViewSet,basename='template')
router.register('spotlight',PostSearchViewSet,basename='spotlight')
router.register('recycle',RecycleViewSet,basename='recycle')

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
#    path('api/getpost/(?P<user>[^/.]+)/(?P<post>[^/.]+)/$', retrievePost, name='getpost'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('account/', include('djoser.urls'),name='auth'),
    path('auth/', include('djoser.urls.jwt'),name='auth-jwt'),
    path('api/auth/oauth/login/', SocialLoginView.as_view()),
    path('api/auth/oauth/', include('rest_framework_social_oauth2.urls')),
    path('api/timeline/',TimelineView.as_view(),name='timeline'),
    path('api/comments/',CommentView.as_view(),name='comments')
    #url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
    #url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
