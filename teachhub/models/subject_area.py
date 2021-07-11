from django.db import models
from teachhub.models.school_classification import SchoolClassification


class SubjectArea(models.Model):

    class Meta:
        db_table = 'subject_areas'

    name = models.CharField(
        verbose_name='教科名', max_length=128, null=False, blank=False, default='')

    school_classification = models.ForeignKey(SchoolClassification, verbose_name='学校区分',
                                              on_delete=models.PROTECT, related_name='subject_areas')

    def __str__(self):
        return self.name
