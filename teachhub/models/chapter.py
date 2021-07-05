from django.db import models
from teachhub.models.textbook import Textbook


class Chapter(models.Model):

    class Meta:
        db_table = 'chapters'

    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                                 on_delete=models.PROTECT, related_name='chapters')

    name = models.CharField(
        verbose_name='章', max_length=128, null=False, blank=True)

    def __str__(self):
        return self.name
