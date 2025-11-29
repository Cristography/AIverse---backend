from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tag, Taggable
from .serializers import TagSerializer, TaggableSerializer
from accounts.permissions import IsModeratorOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsModeratorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all items tagged with this tag"""
        tag = self.get_object()
        taggables = Taggable.objects.filter(tag=tag)
        serializer = TaggableSerializer(taggables, many=True)
        return Response(serializer.data)
