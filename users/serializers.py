from rest_framework import serializers
from .models import User, Payment


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'city', 'avatar']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PaymentShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для истории платежей"""
    paid_item_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'payment_date', 'amount', 'payment_method', 'status', 'paid_item_name']

    def get_paid_item_name(self, obj):
        if obj.course:
            return obj.course.title
        elif obj.lesson:
            return obj.lesson.title
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    payments_history = PaymentShortSerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'payments_history']
        read_only_fields = ['id', 'email', 'payments_history']


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'city', 'avatar']


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    paid_item_name = serializers.SerializerMethodField()
    paid_item_type = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'user_name', 'payment_date',
            'course', 'lesson', 'paid_item_name', 'paid_item_type',
            'amount', 'payment_method', 'status', 'stripe_session_url'
        ]
        read_only_fields = ['payment_date', 'stripe_session_url']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email

    def get_paid_item_name(self, obj):
        if obj.course:
            return obj.course.title
        elif obj.lesson:
            return obj.lesson.title
        return None

    def get_paid_item_type(self, obj):
        if obj.course:
            return 'course'
        elif obj.lesson:
            return 'lesson'
        return None
