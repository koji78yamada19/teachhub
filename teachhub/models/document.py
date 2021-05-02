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

    # ファイルのアップロード先
    # def upload_path(self, filename):
    #     # docx = ['ファイル名', 'docx'][-1]
    #     ext = filename.split('.')[-1]
    #     # 'uuid' + '.' + 'docx'
    #     name = "%s.%s" % (uuid.uuid4(), ext)
    #     # documents の中に name（ファイル）を入れてね
    #     # upload path -> media/documents/uuid.docx
    #     return os.path.join('documents', name)

    # ファイルのアップロード先
    def upload_path(self, filename):
        lst = filename.split(".")
        print("lst")
        print(lst)
        user_id = lst[0]
        filename = lst[1]
        current_time = lst[2]
        path = "documents/notes/"

        return 'documents/notes/{0}_{1}/word/{2}.docx'.format(user_id, filename, current_time)

    # フィールドは chapter_id として生成される
    # 参照 document.chapter.name
    # 逆参照 chapter.document.all()     related_name 逆参照 -> 章から資料を参照
    section = models.ForeignKey(Section, verbose_name='節',
                                on_delete=models.PROTECT, related_name='documents', default=1)

    chapter = models.ForeignKey(Chapter, verbose_name='章',
                                on_delete=models.PROTECT, related_name='documents', default=1)

    textbook = models.ForeignKey(Textbook, verbose_name='教科書',
                                 on_delete=models.PROTECT, related_name='documents', default=1)

    name = models.CharField(
        verbose_name='資料名', max_length=128, null=True, blank=True)

    content = models.TextField(verbose_name='資料説明', null=True, blank=True)

    file = models.FileField(
        verbose_name='ファイル', upload_to=upload_path, null=True, blank=True)

    category = models.CharField(
        verbose_name='カテゴリー', max_length=128, null=True, blank=True)

    updated_by = models.TextField(
        verbose_name='更新者', null=True, blank=True, default=1)

    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    created_by = models.TextField(
        verbose_name='作成者', null=True, blank=True, default=1)

    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

# 追加
    doc_pdf_url = models.TextField(
        verbose_name='pdfファイル', null=True, blank=True)
    diff_word_url = models.TextField(
        verbose_name='差分ファイル', null=True, blank=True)
    diff_pdf_url = models.TextField(
        verbose_name='差分pdfファイル', null=True, blank=True)

    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='user',
                                related_name="document_user", blank=True, null=True)
    latest = models.BooleanField(
        verbose_name='最新のドキュメント', null=True, blank=True, default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return 'documents/1/'
        return reverse('teachhub:document_detail', kwargs={'pk': self.pk})
