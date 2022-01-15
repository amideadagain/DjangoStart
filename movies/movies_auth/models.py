from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, dob, password=None):

        if not email:
            raise ValueError('Email is a mandatory field')
        if not username:
            raise ValueError('Username is a mandatory field')
        if not dob:
            raise ValueError('Date of birth is a mandatory field')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            dob=dob,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, dob, password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            dob=dob,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_user_token_by_credentials(self, username, password):
        user = MyUser.objects.get_by_natural_key(username=username)
        if user.check_password(password):
            return Token.objects.get_or_create(user=user)


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    dob = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    objects = MyUserManager()
    # I wanted to make login with email instead of username (as I did it in path('', views.sign_in, name='sign_in')),
    # but cause of obtain_auth_token which uses username I have to remake it to username again, sad
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'dob']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
