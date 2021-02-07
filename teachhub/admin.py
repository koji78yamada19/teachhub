from django.contrib import admin
from teachhub.models import Document, Chapter, Textbook


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # 教材一覧で表示するフィールド
    list_display = ('name', 'category', 'chapter', 'textbook', 'file')
    # 教材一覧で「詳細」へ進むリンク
    list_display_links = ('name', )
    # 教材一覧で検索対象のフィールド
    search_fields = ('name', 'category', 'chapter__name', 'textbook__name')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    # 教材一覧で表示するフィールド
    list_display = ('name', 'textbook')
    # 教材一覧で「詳細」へ進むリンク
    list_display_links = ('name', )
    # 教材一覧で検索対象のフィールド
    search_fields = ('name', 'textbook__name')

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):

    list_display = ('name', )

    list_display_links = ('name', )

    search_fields = ('name', )