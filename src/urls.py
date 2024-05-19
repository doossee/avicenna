from core.routers import DefaultRouter
from src.management.urls import router as management_router
from src.forum.urls import router as forum_router


router = DefaultRouter()

router.extend(management_router)
router.extend(forum_router)


