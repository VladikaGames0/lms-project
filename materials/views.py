from rest_framework import viewsets, generics, permissions as drf_permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Создание и удаление: только не-модераторы (обычные пользователи)
            permission_classes = [drf_permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Редактирование: модератор или владелец
            permission_classes = [drf_permissions.IsAuthenticated, IsModerator() | IsOwner()]
        else:
            # Просмотр: авторизованные могут смотреть все
            permission_classes = [drf_permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Создание: только не-модераторы
            return [drf_permissions.IsAuthenticated(), ~IsModerator()]
        # Список: авторизованные могут смотреть все
        return [drf_permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            # Редактирование: модератор или владелец
            return [drf_permissions.IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.request.method == 'DELETE':
            # Удаление: только владелец (модераторы не могут удалять)
            return [drf_permissions.IsAuthenticated(), IsOwner()]
        else:  # GET, HEAD, OPTIONS
            return [drf_permissions.IsAuthenticated()]