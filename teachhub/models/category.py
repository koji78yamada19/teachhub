from django.db import models


class Category(models.Model): 

    class Meta:
        db_table = 'categories'

    name = models.CharField( 
        verbose_name='資料カテゴリー', max_length=128, null=False, blank=False)
   
    def __str__(self):
        return self.name
