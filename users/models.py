from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    """
    Расширенная модель пользователя, наследующаяся от стандартной модели AbstractUser.
    Добавлены дополнительные поля: email, телефон, город и аватар. Email используется в качестве основного
    поля для входа в систему вместо username.
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_moderator = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Использование email в качестве основного идентификатора для входа.
    REQUIRED_FIELDS = ['username']  # Указание username как обязательного поля при регистрации.


class Payment(models.Model):
    """
    Модель платежа, содержащая информацию о платежах пользователей. Включает в себя ссылки на пользователя,
    курс и урок, за который произведена оплата, сумму платежа и метод оплаты.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateField()
    paid_course = models.ForeignKey('materials.Course', on_delete=models.SET_NULL, null=True, blank=True)
    paid_lesson = models.ForeignKey('materials.Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100, choices=(('cash', 'Cash'), ('transfer', 'Bank Transfer')))
    stripe_session_url = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        """
        Возвращает строковое представление объекта, показывающее пользователя, сумму платежа
        и дату платежа.
        """
        return f"{self.user} - {self.amount} - {self.payment_date}"
