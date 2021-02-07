from django.db import models


class Textbook(models.Model): 

    class Meta:
        db_table = 'textbooks'

    name = models.CharField( 
        verbose_name='教科書', max_length=128, null=False, blank=False)
    
    def __str__(self):
        return self.name