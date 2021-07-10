from django.db import models


class Subject(models.Model):

    class Meta:
        db_table = 'subjects'

    name = models.CharField(
        verbose_name='科目名', max_length=128, null=False, blank=False)

    def __str__(self):
        return self.name
