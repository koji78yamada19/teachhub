from django.db import models
from django.contrib.auth.models import AbstractUser
from teachhub.models.school import School


class CustomUser(AbstractUser):

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    school = models.ForeignKey(School, verbose_name='学校',
                               on_delete=models.PROTECT, null=True, blank=True, related_name='custom_users')

    email = models.EmailField(verbose_name='メールアドレス',
                              help_text='必須', unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
