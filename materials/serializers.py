from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model"""
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'course_title']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model with lessons count and lessons list"""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        """Return the number of lessons in the course"""
        return obj.lessons.count()