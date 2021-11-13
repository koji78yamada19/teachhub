from django.db import models
from teachhub.models.subject_area import SubjectArea, SchoolClassification


class Subject(models.Model):

    class Meta:
        db_table = 'subjects'

    name = models.CharField(
        verbose_name='科目名', max_length=128, null=False, blank=False, default='')

    subject_area = models.ForeignKey(SubjectArea, verbose_name='教科名',
                                     on_delete=models.PROTECT, related_name='subjects')

    school_classification = models.ForeignKey(SchoolClassification, verbose_name='学校区分',
                                              on_delete=models.PROTECT, related_name='subjects')

    def __str__(self):
        return self.name
