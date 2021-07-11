from django.db import models


class SchoolClassification(models.Model):

    class Meta:
        db_table = 'school_classifications'

    name = models.CharField(
        verbose_name='学校区分', max_length=128, null=False, blank=False, default='')

    def __str__(self):
        return self.name
