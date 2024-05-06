import re
from rest_framework import serializers


def validate_video_url(value):
    # Если значение пустое или None, просто возвращаем его (пропускаем валидацию)
    if not value:
        return

    # Регулярное выражение для проверки URL YouTube
    youtube_regex = r'^https?://(?:www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+$'

    # Если значение не соответствует регулярному выражению, вызываем исключение
    if not re.match(youtube_regex, value):
        raise serializers.ValidationError("Ссылка должна быть на видео с YouTube.com.")
