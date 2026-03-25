from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView, SubscriptionView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    # Сначала идут специфичные маршруты (subscribe), потом router
    path('courses/subscribe/', SubscriptionView.as_view(), name='course-subscribe'),
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]