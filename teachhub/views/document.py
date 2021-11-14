import os

from django.db import reset_queries
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse  # function の中で書くとき（評価タイミングの違い）
from django.contrib.auth.decorators import login_required

from teachhub.models import Textbook, Chapter, Section, Document, Subject
from accounts.models import CustomUser

import requests
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.http import FileResponse


#############
# Read 一覧 #
#############
# 資料一覧ビュー

def document_list(request):
    if request.method == 'GET':
        document_list = Document.objects.all()
        return render(
            request,
            'teachhub/document_list.html',
            dict(document_list=document_list)
        )

#############
# Read 詳細 #
#############


@login_required
# def document_detail(request, pk):
def get_document(request, pk):
    # 教材の詳細を表示(pdfとして表示)
    if request.method == 'GET':
        document = get_object_or_404(Document, pk=pk)
        path = document.path

        url = 'https://prod-22.japanwest.logic.azure.com:443/workflows/e549f57770b24d1f8255ccb2ab1fc8fb/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=VTVnuk1nJXTihBEMQl25PRcjBrOaqbYu7u1h9kTBrqQ'
        data = {'path': path}
        res = requests.post(url, data=data)

        context = {
            'document': document,
            'file_link': res.text
        }
        return render(
            request,
            'teachhub/document_detail.html',
            context
        )

##################################
# Read 資料一覧 / アップロード資料 #
##################################


@login_required
# def document_note(request, section_id):
def upload_and_get_documents(request, subject_id, textbook_id, section_id):
    category_in_path = request.path.split('/')[-2]
    if category_in_path == 'notes':
        category = "板書案"
    elif category_in_path == 'tests':
        category = "小テスト"

    section = Section.objects.get(id=section_id)
    section_name = section.name
    chapter = section.chapter
    chapter_name = chapter.name
    textbook = chapter.textbook
    textbook_name = textbook.name
    subject = Subject.objects.get(id=subject_id)
    subject_name = subject.name

    if request.method == 'GET':
        documents = Document.objects.filter(
            category=category, section=section).order_by('id')
        name_and_docs = []
        for document in documents:
            user = document.user
            custom_user = CustomUser.objects.get(email=user)
            name_and_docs.append({
                "name": custom_user.username,
                "document": document
            })

        context = {
            "name_and_docs": name_and_docs,
            "textbook_name": textbook_name,
            "chapter_name": chapter_name,
            "section_name": section_name,
        }

        if category == '板書案':
            template = 'teachhub/document_note.html'
        elif category == '小テスト':
            template = 'teachhub/document_test.html'

        return render(request, template, context)

    else:
        f = request.FILES.get('file')
        document_name = request.FILES['file'].name
        user_id = request.user.id
        path = f'/documents/{subject_name}/{textbook_name}/{chapter_name}_{section_name}/{category_in_path}/user_{user_id}'

        url = 'https://prod-17.japanwest.logic.azure.com:443/workflows/aa397302f6694e959fca72dbab910124/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=g3Lk7aJOmOEkAWksX_5rcZjCTHIMNo0OShp8pLHYsnw'
        files = {'file': (document_name, f, 'multipart/form-data')}
        data = {
            'title': document_name,
            'path': path
        }
        requests.post(url, files=files, data=data)

        JST = timezone(timedelta(hours=+9), 'JST')
        date = datetime.now(JST)

        custom_user = CustomUser.objects.get(id=user_id)
        name = document_name.split('.')[0]
        try:
            document = Document.objects.get(
                category=category, section=section, user=custom_user, name=name)
            document.updated_by = date
            document.updated_at = custom_user.username
        except:
            document = Document(
                name=name,
                category=category,
                path=f'{path}/{document_name}',
                subject=subject,
                textbook=textbook,
                chapter=chapter,
                section=section,
                content='',
                user=custom_user,
                updated_by=custom_user.username,
                updated_at=date,
                created_by=custom_user.username,
                created_at=date
            )
        document.save()

        if category == '板書案':
            revers_url = 'teachhub:document_note'
        elif category == '小テスト':
            revers_url = 'teachhub:document_test'

        return redirect(reverse(revers_url, args=(subject_id, textbook_id, section_id)))


###############
# Delete 削除 #
###############
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    subject_id = document.subject.id
    textbook_id = document.textbook.id
    section_id = document.section.id
    context = {'document': document}

    if request.method == 'GET':
        return render(
            request,
            'teachhub/document_confirm_delete.html',
            context
        )
    elif request.method == 'POST':
        path = document.path

        url = 'https://prod-15.japanwest.logic.azure.com:443/workflows/3983ac8d86ed41eba9336be99a07ede6/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=zFFWcxkrq4td3xDZ6UT8LTVIo-dL4Z8i21hC2S6eTqw'
        data = {'path': path}
        requests.post(url, data=data)

        document.delete()
        return redirect(reverse('teachhub:document_note', args=(subject_id, textbook_id, section_id,)))


def download_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    path = document.path

    url = 'https://prod-01.japanwest.logic.azure.com:443/workflows/471d46fc40cc4a64a3abe71adbec1fa9/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=z0FgPb_kOXJudulNY3fyAm1Qkzcnkwd8xN5B7ebAdBI'
    data = {'path': path}
    res = requests.post(url, data=data)

    document_name = document.name
    f = open(f'{document_name}.docx', mode='wb+')
    f.write(res.content)
    f.seek(0)
    f.close
    os.remove(f'./{document_name}.docx')

    return FileResponse(f)

# 以下、使っていない


def context_to_show_pdf(document, pdf_url):
    # pdfをブラウザで表示するためにpdf.jsを使用
    # pdfを表示するためのviewerのpath
    viewer_path = "/static/teachhub/pdfjs-2.7.570-dist/web/viewer.html"
    pdf_path = "media/" + str(pdf_url)
    path = viewer_path + "?file=%2F" + pdf_path

    context = {
        'document': document,
        "path": path
    }

    return context


@login_required
def get_history(request, doc_id):
    user = request.user
    print(user)
    document = Document.objects.get(id=doc_id)
    section = document.section
    document_name = document.name
    documents = Document.objects.filter(
        custom_user=user, section=section, name=document_name).order_by('-id')
    histories = documents.values(
        'id', 'doc_pdf_url', 'diff_word_url', 'created_at', 'custom_user')
    lst_histories = list(histories)
    context = {'lst_histories': lst_histories}

    return context


@login_required
def render_history(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    pdf_url = document.doc_pdf_url
    context = context_to_show_pdf(document, pdf_url)
    context_histories = get_history(request, doc_id)
    context.update(context_histories)

    return render(request, 'teachhub/history.html', context)


# def document_create(request):
#     if request.method == 'GET':
#         form = DocumentForm()
#         return render(
#             request,
#             'teachhub/document_form.html',
#             dict(form=form)
#         )
#     elif request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(form.instance.get_absolute_url())
#         else:
#             return render(
#                 request,
#                 'teachhub/document_form.html',
#                 dict(form=form)
#             )


###############
# Update 編集 #
###############
# def update_document(request, doc_id):
#     # ↓ データベースから与えられたid番号を取得(if文の外に書く)
#     document = get_object_or_404(Document, id=doc_id)  # /documents/4/update
#     if request.method == 'GET':
#         form = DocumentForm(instance=document)
#         return render(
#             request,
#             'teachhub/document_form.html',
#             dict(form=form)
#         )
#     elif request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES, instance=document)
#         if form.is_valid():
#             form.save()
#             return redirect(form.instance.get_absolute_url())
#         else:
#             return render(
#                 request,
#                 'teachhub/document_form.html',
#                 dict(form=form)
    # )
