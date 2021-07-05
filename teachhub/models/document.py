import os
import uuid
from django.db import models
from django.urls import reverse
from teachhub.models.section import Section
from teachhub.models.chapter import Chapter
from teachhub.models.textbook import Textbook
from accounts.models import CustomUser


class Document(models.Model):
    class Meta:
        # データ取得時の並び替え
        ordering = ['created_at']
        # テーブル名
        db_table = 'documents'

    # def upload_path(self, filename):
    #     # docx = ['ファイル名', 'docx'][-1]
    #     ext = filename.split('.')[-1]
    #     # 'uuid' + '.' + 'docx'
    #     name = "%s.%s" % (uuid.uuid4(), ext)
    #     # documents の中に name（ファイル）を入れてね
    #     # upload path -> media/documents/uuid.docx
    #     return os.path.join('documents', name)

    # フィールドは chapter_id として生成される
    # 参照 document.chapter.name
    # 逆参照 chapter.document.all()     related_name 逆参照 -> 章から資料を参照
    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                                 on_delete=models.PROTECT, related_name='documents')

    chapter = models.ForeignKey(Chapter, verbose_name='章',
                                on_delete=models.PROTECT, related_name='documents')

    section = models.ForeignKey(Section, verbose_name='節',
                                on_delete=models.PROTECT, related_name='documents')

    name = models.CharField(
        verbose_name='資料名', max_length=128, null=False, blank=True, default='')

    content = models.TextField(
        verbose_name='資料説明', null=False, blank=True, default='')

    # file = models.FileField(
    #     verbose_name='ファイル', upload_to=upload_path, null=True, blank=True)
    path = models.TextField(
        verbose_name='保存先', null=False, blank=True, default='')

    category = models.CharField(
        verbose_name='カテゴリー', max_length=128, null=False, blank=True, default='')

    updated_by = models.TextField(
        verbose_name='更新者', null=False, blank=True, default='')

    updated_at = models.DateTimeField(
        verbose_name='更新日時', null=False, auto_now=True)

    created_by = models.TextField(
        verbose_name='作成者', null=False, blank=True, default='')

    created_at = models.DateTimeField(
        verbose_name='作成日時', null=False, auto_now_add=True)

    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='user',
                                    related_name="document_user", null=True, blank=True, default='')
    # latest = models.BooleanField(
    #     verbose_name='最新のドキュメント', null=True, blank=True, default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return 'documents/1/'
        return reverse('teachhub:document_detail', kwargs={'pk': self.pk})
