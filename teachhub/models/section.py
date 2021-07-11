from django.db import models
from teachhub.models.chapter import Chapter
from teachhub.models.textbook import Textbook
from teachhub.models.subject import Subject


class Section(models.Model):

    class Meta:
        db_table = 'sections'

    name = models.CharField(
        verbose_name='節', max_length=128, null=False, blank=False, default='')

    chapter = models.ForeignKey(Chapter, verbose_name='章',
                                on_delete=models.PROTECT, related_name='sections')

    subject = models.ForeignKey(Subject, verbose_name='科目',
                                on_delete=models.PROTECT, related_name='sections')

    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                                 on_delete=models.PROTECT, related_name='sections')

    def __str__(self):
        return self.name
