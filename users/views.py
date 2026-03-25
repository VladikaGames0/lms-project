from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User, Payment
from .serializers import UserProfileSerializer, PaymentSerializer


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


class PaymentListView(generics.ListAPIView):
    """
    Эндпоинт для вывода списка платежей с фильтрацией.
    GET /api/payments/

    Параметры фильтрации:
    - ordering: порядок сортировки по дате ('payment_date' или '-payment_date')
    - course: ID курса
    - lesson: ID урока
    - payment_method: способ оплаты ('cash' или 'transfer')
    """
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Payment.objects.all()

        # Фильтрация по курсу
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Фильтрация по уроку
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)

        # Фильтрация по способу оплаты
        payment_method = self.request.query_params.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        # Сортировка
        ordering = self.request.query_params.get('ordering', '-payment_date')
        if ordering in ['payment_date', '-payment_date']:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-payment_date')

        return queryset