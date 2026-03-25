from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import User, Payment
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer,
    UserPublicSerializer, PaymentSerializer
)
from .services import (
    create_stripe_product, create_stripe_price,
    create_stripe_checkout_session, get_stripe_session_status
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, status='pending')
        product_id = create_stripe_product(payment)
        payment.stripe_product_id = product_id
        price_id = create_stripe_price(product_id, float(payment.amount))
        payment.stripe_price_id = price_id
        success_url = self.request.build_absolute_uri(reverse('users:payment-success', args=[payment.id]))
        cancel_url = self.request.build_absolute_uri(reverse('users:payment-cancel', args=[payment.id]))
        session_id, session_url = create_stripe_checkout_session(price_id, payment.id, success_url, cancel_url)
        payment.stripe_session_id = session_id
        payment.stripe_session_url = session_url
        payment.save()
        return payment

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = self.perform_create(serializer)
        return Response({
            'payment_id': payment.id,
            'payment_url': payment.stripe_session_url,
            'message': 'Перенаправьте пользователя на payment_url для оплаты'
        }, status=status.HTTP_201_CREATED)


class PaymentStatusView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()
        if payment.stripe_session_id:
            stripe_status = get_stripe_session_status(payment.stripe_session_id)
            if stripe_status.get('payment_status') == 'paid':
                payment.status = 'paid'
                payment.save()
        return Response({
            'payment_id': payment.id,
            'status': payment.status,
            'amount': payment.amount,
            'paid_item': payment.course.title if payment.course else (payment.lesson.title if payment.lesson else None),
            'payment_url': payment.stripe_session_url
        })


class PaymentSuccessView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        payment.status = 'paid'
        payment.save()
        return Response({'message': 'Оплата успешно завершена!', 'payment_id': payment.id})


class PaymentCancelView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        payment.status = 'cancelled'
        payment.save()
        return Response({'message': 'Оплата отменена', 'payment_id': payment.id})