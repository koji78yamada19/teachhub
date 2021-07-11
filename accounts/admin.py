from django.contrib import admin
from .models import CustomUser
from teachhub.models import School

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'school')
    ordering = ['id', ]
    list_display_links = ('username', 'school')
    # 教材一覧で検索対象のフィールド
    search_fields = ('username', 'school__name')
