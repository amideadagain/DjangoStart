from django.test import TestCase

from movies_auth.models import MyUser as User
from movies_auth.tasks import notify_user


class TasksTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='TestDude',
            email='testmail@gmail.com',
            dob='2000-01-08',
            password='testword'
        )
        User.objects.create_user(
            username='TestDude2',
            email='testmail2@gmail.com',
            dob='2001-05-05',
            password='test5221'
        )
        User.objects.create_user(
            username='TestDude3',
            email='testmail3@gmail.com',
            dob='2000-10-07',
            password='test7432'
        )

    def test_notify_user_task(self):
        message = notify_user()
        users = User.objects.all()
        for user in users.iterator():
            self.assertTrue(user.is_notified)
        self.assertEqual(message, "Notified the users")
