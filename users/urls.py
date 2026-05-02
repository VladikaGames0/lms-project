from django.urls import path
from .views import (
    UserRegistrationView, UserProfileView, UserDetailView,
    PaymentListView, CreatePaymentView, PaymentStatusView,
    PaymentSuccessView, PaymentCancelView
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', CreatePaymentView.as_view(), name='payment-create'),
    path('payments/<int:pk>/status/', PaymentStatusView.as_view(), name='payment-status'),
    path('payments/<int:payment_id>/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payments/<int:payment_id>/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]
