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

import config

#############
# Read 詳細 #
#############


@ login_required
def get_document(request, pk):
    # 教材の詳細を表示(pdfとして表示)
    if request.method == 'GET':
        document = get_object_or_404(Document, pk=pk)
        path = document.path

        url = 'https://prod-24.japanwest.logic.azure.com:443/workflows/a2ac6b9aec134e4b99d4071d02859493/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=BwqnTKq9rWOcZjbRPVjfMnJXW-wTm01Wv95HECOt4Ow'
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


@ login_required
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

        # local_settings.pyが存在する場合は開発用のパスにファイルをアップロードする
        if os.path.exists(config.settings.f):
            path = f'/documents/dev/{subject_name}/{textbook_name}/{chapter_name}_{section_name}/{category_in_path}/user_{user_id}'
        else:
            path = f'/documents/{subject_name}/{textbook_name}/{chapter_name}_{section_name}/{category_in_path}/user_{user_id}'

        url = 'https://prod-28.japanwest.logic.azure.com:443/workflows/9f34d912159c4d7ba3c462afaa52ecf9/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=603MhfXHajXmggxonmy8B9aoHyzIopTHAlfus2E4Tzw'
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

        url = 'https://prod-28.japanwest.logic.azure.com:443/workflows/e0424ea9f4b14f9c9fd4d450f8fb4ddf/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=tarWtYTcdO9oU4vR20raM7bXd26S17e7pRJuBCjz5ZI'
        data = {'path': path}
        requests.post(url, data=data)

        document.delete()
        return redirect(reverse('teachhub:document_note', args=(subject_id, textbook_id, section_id,)))


def download_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    path = document.path

    url = 'https://prod-18.japanwest.logic.azure.com:443/workflows/147e2b6620bf4047aa7a3cdc1013e225/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=YIzHfryDtIBc3yrneoKai_fAV4qPHbtWy2U82bCTr8s'
    data = {'path': path}
    res = requests.post(url, data=data)

    document_name = document.name
    f = open(f'{document_name}.docx', mode='wb+')
    f.write(res.content)
    f.seek(0)
    f.close
    os.remove(f'./{document_name}.docx')

    return FileResponse(f)
