from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Prompt, PromptRelation
from .serializers import PromptSerializer, PromptCreateUpdateSerializer, PromptRelationSerializer
from accounts.permissions import IsOwnerOrReadOnly, CanModerateContent
from django.db import models

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.select_related('author').all()
    permission_classes = [IsAuthenticatedOrReadOnly, CanModerateContent]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'author__username']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'views', 'title']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PromptCreateUpdateSerializer
        return PromptSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def relations(self, request, slug=None):
        prompt = self.get_object()
        relations = PromptRelation.objects.filter(source_prompt=prompt).select_related(
            'target_prompt__author'
        )
        serializer = PromptRelationSerializer(relations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_prompts(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        prompts = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(prompts)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, slug=None):
        prompt = self.get_object()  # Will 404 if slug not found
        prompt.views = models.F('views') + 1
        prompt.save(update_fields=['views'])
        prompt.refresh_from_db()
        return Response({'views': prompt.views})
