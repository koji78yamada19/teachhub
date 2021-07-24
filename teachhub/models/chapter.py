from django.db import models
from teachhub.models.textbook import Textbook
from teachhub.models.subject import Subject


class Chapter(models.Model):

    class Meta:
        db_table = 'chapters'

    name = models.CharField(
        verbose_name='章', max_length=128, null=False, blank=True)

    subject = models.ForeignKey(Subject, verbose_name='科目',
                                on_delete=models.PROTECT, related_name='chapters', default='')

    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                                 on_delete=models.PROTECT, related_name='chapters', default='')

    def __str__(self):
        return self.name
