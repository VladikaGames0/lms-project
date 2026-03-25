from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Payment
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserPublicSerializer, PaymentSerializer
from .permissions import IsModerator


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Payment.objects.all()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        payment_method = self.request.query_params.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        ordering = self.request.query_params.get('ordering', '-payment_date')
        if ordering in ['payment_date', '-payment_date']:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-payment_date')
        return queryset