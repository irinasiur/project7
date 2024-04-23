from django.core.management.base import BaseCommand
from users.models import User
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Initializes the database with sample data.'

    def handle(self, *args, **options):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        course = Course.objects.create(title='Example Course', description='A sample course for testing.')
        Lesson.objects.create(course=course, title='Introduction', description='An introductory lesson.')
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial data.'))
