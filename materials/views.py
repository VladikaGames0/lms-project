from rest_framework import viewsets, generics, permissions as drf_permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CoursePaginator, LessonPaginator
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [drf_permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [drf_permissions.IsAuthenticated]
        else:
            permission_classes = [drf_permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_permissions(self):
        if self.request.method == 'POST':
            return [drf_permissions.IsAuthenticated()]
        return [drf_permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [drf_permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [drf_permissions.IsAuthenticated()]
        else:
            return [drf_permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        lesson = self.get_object()
        user = self.request.user
        is_moderator = user.groups.filter(name='moderators').exists()

        if is_moderator or lesson.owner == user:
            serializer.save()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("У вас нет прав на редактирование этого урока")

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.owner == user:
            instance.delete()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("У вас нет прав на удаление этого урока")


class SubscriptionView(APIView):
    """
    Эндпоинт для управления подписками на курс
    POST /api/courses/subscribe/ - добавить/удалить подписку
    """
    permission_classes = [drf_permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
            status_code = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)