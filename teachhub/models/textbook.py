from django.db import models
from teachhub.models.subject import Subject
from teachhub.models.school_classification import SchoolClassification
from teachhub.models.school import School


class Textbook(models.Model):

    class Meta:
        db_table = 'textbooks'

    name = models.CharField(
        verbose_name='教科書', max_length=128, null=False, blank=False, default='')

    subject = models.ForeignKey(Subject, verbose_name='科目',
                                on_delete=models.PROTECT, related_name='textbooks')

    school_classification = models.ForeignKey(SchoolClassification, verbose_name='学校区分',
                                              on_delete=models.PROTECT, related_name='textbooks')

    school = models.ManyToManyField(School, verbose_name='学校')

    def __str__(self):
        return self.name
