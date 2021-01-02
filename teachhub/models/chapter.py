from django.db import models


class Chapter(models.Model): 

    class Meta:
        db_table = 'chapters'

    name = models.CharField( 
        verbose_name='章', max_length=128, null=False, blank=False)
    
    def __str__(self):
        return self.name