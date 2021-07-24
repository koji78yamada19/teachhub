from django.contrib import admin
from .models import CustomUser
from teachhub.models import School

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'school')
    ordering = ['id', ]
    list_display_links = ('email', 'username', 'school')
    # 教材一覧で検索対象のフィールド
    search_fields = ('email', 'username', 'school__name')
