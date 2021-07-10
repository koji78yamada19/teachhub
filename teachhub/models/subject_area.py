from django.db import models


class SubjectArea(models.Model):

    class Meta:
        db_table = 'subject_areas'

    subject_area_name = models.CharField(
        verbose_name='教科名', max_length=128, null=False, blank=False)

    def __str__(self):
        return self.subject_area_name
