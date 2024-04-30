from django.contrib.auth import get_user_model
from django.db import models

from config import settings

User = get_user_model()


# Create your models here.
class Course(models.Model):
    """
        Представляет курс, содержащий несколько уроков.

        Атрибуты:
            title (models.CharField): Название курса, ограниченное 150 символами.
            description (models.TextField): Подробное описание содержания курса.
            preview (models.ImageField): Необязательное поле изображения, позволяющее загружать предварительный просмотр курса.
    """
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='course_previews/', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', on_delete=models.CASCADE,
                              verbose_name='владелец')

    def __str__(self):
        """
            Возвращает строковое представление экземпляра Course, которое является названием курса.
        """
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """
    Представляет урок, принадлежащий курсу.

    Атрибуты:
        course (models.ForeignKey): Внешний ключ, связывающий с соответствующим курсом.
                                   С помощью related_name 'lessons' можно обращаться к урокам из экземпляра курса.
        title (models.CharField): Название урока, ограниченное 200 символами.
        description (models.TextField): Подробное описание содержания урока.
        preview (models.ImageField): Необязательное поле изображения, позволяющее загружать предварительный просмотр урока.
        video_url (models.URLField): Необязательное поле URL, для ссылки на внешнее видео, связанное с уроком.
    """
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lessons', on_delete=models.CASCADE,
                              verbose_name='владелец')

    def __str__(self):
        """
        Возвращает строковое представление экземпляра Lesson, которое является названием урока.
        """
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
