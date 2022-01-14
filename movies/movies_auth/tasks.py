from celery import shared_task
from movies_auth.models import MyUser as User


@shared_task
def notify_user():
    users = User.objects.all()
    for user in users.iterator():
        if not user.is_notified:
            user.is_notified = True
            user.save()
    return "Notified the users"
