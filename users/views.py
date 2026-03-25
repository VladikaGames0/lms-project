from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт для просмотра и редактирования профиля пользователя.
    GET /api/users/profile/ - получить профиль
    PATCH /api/users/profile/ - обновить профиль
    """
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                email='test@example.com',
                password='test123',
                first_name='Test',
                last_name='User'
            )
        return user