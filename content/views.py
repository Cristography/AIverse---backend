from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Blog, News, Tool, ToolType
from .serializers import (
    BlogSerializer, BlogCreateUpdateSerializer,
    NewsSerializer, NewsCreateUpdateSerializer,
    ToolSerializer, ToolCreateUpdateSerializer,
    ToolTypeSerializer
)
from accounts.permissions import IsModeratorOrReadOnly, CanModerateContent
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status  



class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.select_related('author').all()
    permission_classes = [IsModeratorOrReadOnly, CanModerateContent]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogCreateUpdateSerializer
        return BlogSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

"""     @action(detail=True, methods=['post'])
    def increment_view(self, request, slug=None):
        try:
            blog = self.get_object()
            blog.views = models.F('views') + 1
            blog.save(update_fields=['views'])
            blog.refresh_from_db()  
            return Response({'views': blog.views}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 """
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.select_related('author').all()
    permission_classes = [IsModeratorOrReadOnly, CanModerateContent]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NewsCreateUpdateSerializer
        return NewsSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.select_related('author', 'type').all()
    permission_classes = [IsModeratorOrReadOnly, CanModerateContent]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ToolCreateUpdateSerializer
        return ToolSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, slug=None):
        tool = self.get_object()
        tool.views = models.F('views') + 1
        tool.save(update_fields=['views'])
        tool.refresh_from_db()
        return Response({'views': tool.views}, status=status.HTTP_200_OK)
class ToolTypeViewSet(viewsets.ModelViewSet):
    queryset = ToolType.objects.all()
    serializer_class = ToolTypeSerializer
    permission_classes = [IsModeratorOrReadOnly]