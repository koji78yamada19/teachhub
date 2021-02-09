import os
import uuid
from django.db import models
from django.urls import reverse
from teachhub.models.chapter import Chapter
from teachhub.models.textbook import Textbook


class Document(models.Model):

    class Meta:
        # データ取得時の並び替え
        ordering = ['created_at']
        # テーブル名
        db_table = 'documents'

    # ファイルのアップロード先
    def upload_path(self, filename):
        # docx = ['ファイル名', 'docx'][-1]
        ext = filename.split('.')[-1]
        # 'uuid' + '.' + 'docx'
        name = "%s.%s" % (uuid.uuid4(), ext)
        # documents の中に name（ファイル）を入れてね
        # upload path -> media/documents/uuid.docx
        return os.path.join('documents', name)

    # フィールドは chapter_id として生成される 
    # 参照 document.chapter.name
    # 逆参照 chapter.document.all()     related_name 逆参照 -> 章から資料を参照
    chapter = models.ForeignKey(Chapter, verbose_name='章',
                            on_delete=models.PROTECT, related_name='documents', default=1)
    
    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                            on_delete=models.PROTECT, related_name='documents', default=1)

    name = models.CharField(
        verbose_name='資料名', max_length=128, null=False, blank=False)

    content = models.TextField(verbose_name='資料説明', null=False, blank=False)

    file = models.FileField(
        verbose_name='ファイル', upload_to=upload_path, null=False, blank=False)
    
    category = models.CharField(
        verbose_name='カテゴリー', max_length=128, null=False, blank=False)

    updated_by = models.TextField(verbose_name='更新者', null=False, blank=False, default=1)

    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    created_by = models.TextField(verbose_name='作成者', null=False, blank=False, default=1)

    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return 'documents/1/'
        return reverse('teachhub:document_detail', kwargs={'pk': self.pk})