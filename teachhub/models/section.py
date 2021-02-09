from django.db import models
from teachhub.models.chapter import Chapter


class Section(models.Model): 

    class Meta:
        db_table = 'sections'

    chapter = models.ForeignKey(Chapter, verbose_name='章',
                            on_delete=models.PROTECT, related_name='sections')

    name = models.CharField( 
        verbose_name='節', max_length=128, null=False, blank=False)
    
    def __str__(self):
        return self.name