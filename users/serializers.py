from rest_framework import serializers
from .models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar']
        read_only_fields = ['id', 'email']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    paid_item_name = serializers.SerializerMethodField()
    paid_item_type = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'user_name', 'payment_date',
            'course', 'lesson', 'paid_item_name', 'paid_item_type',
            'amount', 'payment_method'
        ]
        read_only_fields = ['payment_date']

    def get_user_name(self, obj):
        """Return full name of the user"""
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email

    def get_paid_item_name(self, obj):
        """Return name of the paid item (course or lesson)"""
        if obj.course:
            return obj.course.title
        elif obj.lesson:
            return obj.lesson.title
        return None

    def get_paid_item_type(self, obj):
        """Return type of the paid item"""
        if obj.course:
            return 'course'
        elif obj.lesson:
            return 'lesson'
        return None