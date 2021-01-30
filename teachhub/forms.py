from teachhub.models import Document
from django import forms

class DocumentForm(forms.ModelForm):

    class Meta:
        # 使用するモデル
        model = Document
        # 使用するフィールド
        fields = ('name', 'chapter', 'category', 'content', 'file')
        