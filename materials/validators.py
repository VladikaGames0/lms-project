import re
from rest_framework import serializers


def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет на youtube.com
    """
    # Регулярное выражение для проверки youtube ссылок
    youtube_pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'

    if value and not re.match(youtube_pattern, value):
        raise serializers.ValidationError(
            "Разрешены только ссылки на YouTube (youtube.com или youtu.be)"
        )
    return value