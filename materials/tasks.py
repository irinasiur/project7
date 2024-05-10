from celery import shared_task
from django.core.mail import send_mail
from .models import CourseSubscription, Course
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


@shared_task
def send_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = CourseSubscription.objects.filter(course=course).select_related('user')

    for subscription in subscribers:
        send_mail(
            'Course Updated',
            f'The course "{course.title}" has been updated.',
            'from@example.com',
            [subscription.user.email],
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    return f'Deactivated {count} users'
