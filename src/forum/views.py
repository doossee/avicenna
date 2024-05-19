from rest_framework import viewsets
from .models import DiseaseCategory, DiseasePost, DiseasePostAttachment, Comment
from .serializers import DiseaseCategorySerializer, DiseasePostSerializer, DiseasePostAttachmentSerializer, CommentSerializer


class DiseaseCategoryViewSet(viewsets.ModelViewSet):
    queryset = DiseaseCategory.objects.all()
    serializer_class = DiseaseCategorySerializer


class DiseasePostViewSet(viewsets.ModelViewSet):
    queryset = DiseasePost.objects.all()
    serializer_class = DiseasePostSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class DiseasePostAttachmentViewSet(viewsets.ModelViewSet):
    queryset = DiseasePostAttachment.objects.all()
    serializer_class = DiseasePostAttachmentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
