from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, NewsViewSet, ToolViewSet, ToolTypeViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'tools', ToolViewSet, basename='tool')
router.register(r'tool-types', ToolTypeViewSet, basename='tool-type')

urlpatterns = [
    path('', include(router.urls)),
]