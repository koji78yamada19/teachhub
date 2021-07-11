from django.db import models


class School(models.Model):

    class Meta:
        db_table = 'schools'

    name = models.CharField(
        verbose_name='学校', max_length=128, null=False, blank=False, default='')

    def __str__(self):
        return self.name
