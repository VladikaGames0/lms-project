from django.urls import path
from .views import UserRegistrationView, UserProfileView, UserDetailView, PaymentListView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]