from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse  # function の中で書くとき（評価タイミングの違い）
# from django.views import generic

from teachhub.models import Textbook, Chapter, Section, Document
from teachhub.forms import DocumentForm

from accounts.models import CustomUser

import win32com.client
import pythoncom
import threading
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
import os
import re
import sys
import shutil
# 開発のため
from django.http import HttpResponseRedirect

#############
# Read 詳細 #
#############

def document_detail(request, pk):
    # 教材の詳細を表示
    if request.method == 'GET':
        # document = Document.objects.get(id=pk)
        document = get_object_or_404(Document, pk=pk)
        pdf_url = document.doc_pdf_url

        viewer_path = "/static/teachhub/pdfjs-2.7.570-dist/web/viewer.html"
        pdf_path = "media/" + str(pdf_url)
        path = viewer_path + "?file=%2F" + pdf_path
 
        context = {
            'document': document,
            "path": path
        }
        # render(request, 'テンプレート名' {'key':'value'})
        return render(
            request,
            'teachhub/document_detail.html',
            context
        )


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

def document_test(request, section_id):
    category = "tests"
    if request.method == 'GET':
        document_test = Document.objects.filter(
            category=category, section_id=section_id)
        section = Section.objects.get(id=section_id)
        section_name = section.name
        context = {"document_test": document_test,
                   "section_name": section_name}
        return render(
            request,
            'teachhub/document_test.html',
            # dict(document_test=document_test)
            context
        )

# wordファイルをpdfファイルに変換
@login_required
def convert_document(request, doc, diff_pdf_url, lock):
    with lock:
        # Wordを起動する前にこれを呼び出す
        pythoncom.CoInitialize()
        # #Wordを起動する : Applicationオブジェクトを生成する
        try:
            Application = win32com.client.gencache.EnsureDispatch(
                "Word.Application")
        except AttributeError:
            # Remove cache and try again.
            MODULE_LIST = [m.__name__ for m in sys.modules.values()]
            for module in MODULE_LIST:
                if re.match(r'win32com\.gen_py\..+', module):
                    del sys.modules[module]
            shutil.rmtree(os.path.join(os.environ.get(
                'LOCALAPPDATA'), 'Temp', 'gen_py'))
            Application = win32com.client.gencache.EnsureDispatch(
                "Word.Application")

        Application.Documents.Open(doc)
        wdFormatPDF = 17
        print("pdf化開始")
        Application.ActiveDocument.SaveAs2(
            FileName=diff_pdf_url, FileFormat=wdFormatPDF)
        print("pdf化終了")

        Application.ActiveDocument.Close()
        #Wordを終了する : Quitメソッドを呼ぶ
        Application.Quit()
        pythoncom.CoUninitialize()

    return ""


# wordファイルの差分を取る
@login_required
def compare_documents(request, original_doc, revised_doc, diff_word_url, lock):

    with lock:
        pythoncom.CoInitialize()
        try:
            Application = win32com.client.gencache.EnsureDispatch(
                "Word.Application")
        except AttributeError:
            MODULE_LIST = [m.__name__ for m in sys.modules.values()]
            for module in MODULE_LIST:
                if re.match(r'win32com\.gen_py\..+', module):
                    del sys.modules[module]
            shutil.rmtree(os.path.join(os.environ.get(
                'LOCALAPPDATA'), 'Temp', 'gen_py'))
            Application = win32com.client.gencache.EnsureDispatch(
                "Word.Application")

        ori_doc_open = Application.Documents.Open(original_doc)
        rev_doc_open = Application.Documents.Open(revised_doc)
        print("差分計算開始")
        Application.CompareDocuments(ori_doc_open, rev_doc_open)
        Application.ActiveDocument.SaveAs2(FileName=diff_word_url)
        print("差分計算終了")

        Application.ActiveDocument.Close()
        Application.Quit()
        pythoncom.CoUninitialize()

    return ""


@login_required
def document_note(request, section_id):
    lock = threading.Lock()
    category = "notes"
    section = Section.objects.get(id=section_id)
    section_name = section.name
    chapter = section.chapter
    chapter_name = chapter.name
    textbook = chapter.textbook
    textbook_name = textbook.name

    if request.method == 'POST':
        JST = timezone(timedelta(hours=+9), 'JST')
        date = datetime.now(JST)
        current_time = date.strftime('%Y-%m-%d-%H-%M-%S')
        print("current_time")
        print(current_time)
        print("request")
        print(request.FILES)
        
        tmp_name_by_writer = request.FILES['file'].name
        name_by_writer = tmp_name_by_writer.split(".")[0]
        request.FILES['file'].name = str(request.user.id) + "." \
                                    + "{}_{}_{}".format(textbook_name, chapter_name, section_name) \
                                    + "." + current_time

        form = DocumentForm(request.POST, request.FILES)

        doc_info = request.FILES['file'].name
        lst_doc_info = doc_info.split(".")
        print("lst_doc_info")
        print(lst_doc_info)

        p2 = ""
        if form.is_valid():
            print("form is valid")
            form.save()
            print("form is saved")

            user_id = lst_doc_info[0]
            print("user_id")
            print(user_id)
            original_doc_name = lst_doc_info[1]

            path = 'documents/notes/{0}_{1}/word/{2}.docx'.format(
                user_id, original_doc_name, current_time)

            base_word_url = r"C:\Users\kojiy\teachhub\media\documents\{}\{}\word\{}.docx"
            # base_diff_word = r"C:\Users\kojiy\teachhub\media\documents\differences\{}\{}\{}.docx"

            doc_name = "{0}_{1}".format(user_id, original_doc_name)
            word_url = base_word_url.format(
                category, doc_name, current_time)
            pdf_url = word_url.replace(
                "word", "pdf").replace(".docx", ".pdf")

            # データベースの更新
            print("DBの更新")
            document = Document.objects.get(file=path)
            custom_user = CustomUser.objects.get(id=user_id)
            document.custom_user = custom_user
            document.created_at = date
            document.name = name_by_writer
            document.category = category
            print(date)
            document.save()
            
            # ファイルのpdf化
            p1 = threading.Thread(target=convert_documents, args=(
            request, word_url, pdf_url, lock))

            # 1つ前のファイルとの差分作成 / そのファイルの保存
            document_id = document.id
            print("id")
            print(document_id)
            documents = Document.objects.filter(custom_user=custom_user)
            document_num = documents.count()
            if document_num > 1:
                # id < doc_id
                pre_document = Document.objects.filter(
                    id__lt=document_id).order_by('-id').first()
                str_document = str(pre_document.file)
                lst_document_info = str_document.split("/")

                # TODO
                # 時間に関する変数の整理
                print("lst_document_info")
                print(lst_document_info)
                category = lst_document_info[1]
                doc_name = lst_document_info[2]
                tmp_time = lst_document_info[-1]

                time = tmp_time.split(".")[0]
                pre_word_url = base_word_url.format(
                    category, doc_name, time)
                base_diff_word_url = r"C:\Users\kojiy\teachhub\media\documents\{}\{}\differences\word\{}.docx"
                diff_word_url = base_diff_word_url.format(
                    category, doc_name, current_time)
                document.diff_word_url = diff_word_url
                document.save()

                p2 = threading.Thread(target=compare_documents, args=(
                    request, pre_word_url, word_url, diff_word_url, lock))

            print("convert_documents started")
            p1.start()
            print("started")

            if p2:
                print("compare_documents started")
                p2.start()

            # 2. そのファイルのurlをDBに格納 update
            print("doc_pdf_url")
            print(pdf_url)
            document.doc_pdf_url = pdf_url
            document.save()
            print("終了")

            return redirect(reverse('teachhub:document_note', args=(section_id,)))
    else:
        # TODO
        # user_idとnameでフィルタリングして、その中で最新のもの
        documents = Document.objects.filter(
            category=category, section_id=section_id).order_by('id')
        form = DocumentForm()
        context = {
            "documents": documents,
            "textbook_name": textbook_name,
            "chapter_name": chapter_name,
            "section_name": section_name,
            'form': form
            }
        
        return render(
            request,
            'teachhub/document_note.html',
            context
        )




# def document_note(request, section_id):
#     if request.method == 'GET':
#         document_note = Document.objects.filter(
#             category='板書案', section_id=section_id).order_by('id')
#         section = Section.objects.get(id=section_id)
#         section_name = section.name
#         context = {"document_note": document_note,
#                    "section_name": section_name}
#         return render(
#             request,
#             'teachhub/document_note.html',
#             context
#         )
#     else:
#         return redirect(reverse('teachhub:upload'))


# category(小テスト）とsection_idでフィルタリングした資料一覧ビュー

###############
# Create 作成 #
###############


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
def update_document(request, pk):
    # ↓ データベースから与えられたid番号を取得(if文の外に書く)
    document = get_object_or_404(Document, pk=pk)  # /documents/4/update
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
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'GET':
        return render(
            request,
            'teachhub/document_confirm_delete.html',
            dict(document=document)
        )
    elif request.method == 'POST':
        document.delete()
        # return rediredt('/documents/')
        return redirect(reverse('teachhub:document_list'))