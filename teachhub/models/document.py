import os
import uuid
from django.db import models
from django.urls import reverse
from teachhub.models.section import Section
from teachhub.models.chapter import Chapter
from teachhub.models.textbook import Textbook
from teachhub.models.subject import Subject
from teachhub.models.school import School
from accounts.models import CustomUser


class Document(models.Model):
    class Meta:
        # データ取得時の並び替え
        ordering = ['created_at']
        # テーブル名
        db_table = 'documents'

    name = models.CharField(
        verbose_name='資料名', max_length=128, null=False, blank=True, default='')

    category = models.CharField(
        verbose_name='カテゴリー', max_length=128, null=False, blank=True, default='')

    path = models.TextField(
        verbose_name='保存先', null=False, blank=True, default='')

    subject = models.ForeignKey(Subject, verbose_name='科目',
                                on_delete=models.PROTECT, related_name='documents')

    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                                 on_delete=models.PROTECT, related_name='documents')

    chapter = models.ForeignKey(Chapter, verbose_name='章',
                                on_delete=models.PROTECT, related_name='documents')

    section = models.ForeignKey(Section, verbose_name='節',
                                on_delete=models.PROTECT, related_name='documents')

    content = models.TextField(
        verbose_name='資料説明', null=False, blank=True, default='')

    updated_by = models.TextField(
        verbose_name='更新者', null=False, blank=True, default='')

    updated_at = models.DateTimeField(
        verbose_name='更新日時', null=False, auto_now=True)

    created_by = models.TextField(
        verbose_name='作成者', null=False, blank=True, default='')

    created_at = models.DateTimeField(
        verbose_name='作成日時', null=False, auto_now_add=True)

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',
                             on_delete=models.PROTECT, related_name='documents')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return 'documents/1/'
        return reverse('teachhub:document_detail', kwargs={'pk': self.pk})
