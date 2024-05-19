from rest_framework.routers import DefaultRouter

from .views import (
    DiseaseCategoryViewSet,
    DiseasePostViewSet,
    DiseasePostAttachmentViewSet,
    CommentViewSet
)

router = DefaultRouter()

router.register(r'disease-categories', DiseaseCategoryViewSet)
router.register(r'disease-posts', DiseasePostViewSet)
router.register(r'disease-post-attachments', DiseasePostAttachmentViewSet)
router.register(r'comments', CommentViewSet)