from django.contrib import admin
from .models import Document, Section, Chapter, Textbook
# from accounts.models import CustomUser


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # 教材一覧で表示するフィールド
    list_display = ('name', 'category', 'section',
                    'chapter', 'textbook')
    # 教材一覧で「詳細」へ進むリンク
    list_display_links = ('name', )
    # 教材一覧で検索対象のフィールド
    search_fields = ('name', 'category', 'section__name',
                     'chapter__name', 'textbook__name')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    list_display = ('name', 'chapter')
    ordering = ['id', ]
    list_display_links = ('name', )

    search_fields = ('name', 'chapter__name')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    # 教材一覧で表示するフィールド
    list_display = ('name', 'textbook')
    ordering = ['id', ]
    # 教材一覧で「詳細」へ進むリンク
    list_display_links = ('name', )
    # 教材一覧で検索対象のフィールド
    search_fields = ('name', 'textbook__name')


@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):

    list_display = ('name', )
    ordering = ['id', ]
    list_display_links = ('name', )

    search_fields = ('name', )


# @admin.register(Textbook)
# class SubjectAreaAdmin(admin.ModelAdmin):

#     list_display = ('name', )
#     ordering = ['id', ]
#     list_display_links = ('name', )

#     search_fields = ('name', )


# @admin.register(Textbook)
# class SubjectAdmin(admin.ModelAdmin):

#     list_display = ('name', )
#     ordering = ['id', ]
#     list_display_links = ('name', )

#     search_fields = ('name', )


# # TODO classにする
# admin.site.register(CustomUser)
