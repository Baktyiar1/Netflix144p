from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        'Имя',
        max_length=123,
        unique=True
    )
    email = models.EmailField(
        'Электронная почта',
        blank=True,
        null=True
    )
    cover = models.ImageField(
        upload_to='media/user_cover/',
        blank=True,
        null=True
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер')
        ),
        default=1,
        verbose_name='Статус пользователя'
    )
    is_admin = models.BooleanField(
        'Администратор',
        default=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'











