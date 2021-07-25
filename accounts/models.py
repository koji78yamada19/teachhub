from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from teachhub.models.school import School


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    username = models.CharField(
        'ユーザー名',
        max_length=150,
        blank=False,
        null=False,
        help_text="半角アルファベット、半角数字、@/./+/-/_ で150文字以下にしてください。",
        validators=[AbstractUser.username_validator],
    )

    email = models.EmailField(verbose_name='メールアドレス',
                              unique=True, null=False, blank=False)

    # school = models.ForeignKey(School, verbose_name='学校',
    #                            on_delete=models.PROTECT, null=True, blank=True, related_name='custom_users')
    school = models.CharField(
        verbose_name='学校名', max_length=128, null=True, blank=True, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
