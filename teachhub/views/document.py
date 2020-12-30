from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse # function の中で書くとき（評価タイミングの違い）
# from django.views import generic

from teachhub.models import Document
# from teachhub.forms import DocumentForm


#############
# Read 詳細 #
#############

# function based view
def document_detail(request, pk):
    # 教材の詳細を表示
    if request.method == 'GET':
        # document = Document.objects.get(id=pk)
        document = get_object_or_404(Document, pk=pk)
        # render(request, 'テンプレート名' {'key':'value'})
        return render(
            request,
            'teachhub/document_detail.html',
            dict(document=document) # -> {'document':'document'}
        )


#############
# Read 一覧 #
#############
def document_list(request):
    if request.method == 'GET':
        document_list = Document.objects.all()
        return render(
            request,
            'teachhub/document_list.html',
            dict(document_list=document_list)
        )




