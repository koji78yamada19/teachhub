from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse # function の中で書くとき（評価タイミングの違い）
# from django.views import generic

from teachhub.models import Document
from teachhub.forms import DocumentForm


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


###############
# Create 作成 #
###############
def document_create(request):
    if request.method == 'GET':
        form = DocumentForm()
        return render(
            request,
            'teachhub/document_form.html',
            dict(form=form)
        )
    elif request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(form.instance.get_absolute_url())
        else:
            return render(
                request,
                'teachhub/document_form.html',
                dict(form=form)
            )


###############
# Update 編集 #
###############
def document_update(request, pk):
    # ↓ データベースから与えられたid番号を取得(if文の外に書く)
    document = get_object_or_404(Document, pk=pk) # /documents/4/update
    if request.method == 'GET':
        form = DocumentForm(instance=document)
        return render(
            request,
            'teachhub/document_form.html',
            dict(form=form)
        )
    elif request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect(form.instance.get_absolute_url())
        else:
            return render(
                request,
                'teachhub/document_form.html',
                dict(form=form)
            )


###############
# Delete 削除 #
###############
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk) 
    if request.method == 'GET':
        return render (
            request,
            'teachhub/document_confirm_delete.html',
            dict(document=document)
        )
    elif request.method == 'POST':
        document.delete()
        # return rediredt('/documents/')
        return redirect(reverse('teachhub:document_list'))


