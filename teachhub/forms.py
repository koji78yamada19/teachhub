from teachhub.models import Document
from django import forms

# class DocumentForm(forms.ModelForm):

#     class Meta:
#         # 使用するモデル
#         model = Document
#         # 使用するフィールド
#         fields = ('name', 'textbook', 'chapter', 'section', 'category', 'content', 'file')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)
        