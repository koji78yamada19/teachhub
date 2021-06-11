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


@login_required
def document_detail(request, pk):
    # 教材の詳細を表示(pdfとして表示)
    if request.method == 'GET':
        # document = Document.objects.get(id=pk)
        document = get_object_or_404(Document, pk=pk)
        pdf_url = document.doc_pdf_url

        context = context_to_show_pdf(document, pdf_url)
        # render(request, 'テンプレート名' {'key':'value'})
        return render(
            request,
            'teachhub/document_detail.html',
            context
        )

# 履歴詳細表示


@login_required
def show_history_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    pdf_url = document.doc_pdf_url

    context = context_to_show_pdf(document, pdf_url)
    # 履歴の情報をコンテクストに追加
    context_histories = get_history(request, doc_id)
    context.update(context_histories)

    return render(request, 'teachhub/history.html', context)

# 差分詳細表示


@login_required
def show_diff(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    diff_word_url = document.diff_word_url
    diff_pdf_url = document.diff_pdf_url

    # 既にpdfがある場合
    if diff_pdf_url:
        pdf_url = diff_pdf_url

        context = context_to_show_pdf(document, pdf_url)
        context_histories = get_history(request, doc_id)
        context.update(context_histories)

        return render(request, 'teachhub/history.html', context)

    # 差分のwordファイルがある場合
    elif diff_word_url:
        if os.path.isfile(diff_word_url):
            lock = threading.Lock()
            diff_pdf_url = diff_word_url.replace(
                "word", "pdf").replace(".docx", ".pdf")
            convert_document(request, diff_word_url, diff_pdf_url, lock)
            document.diff_pdf_url = diff_pdf_url
            document.save()
            pdf_url = diff_pdf_url

            context = context_to_show_pdf(document, pdf_url)
            context_histories = get_history(request, doc_id)
            context.update(context_histories)

            return render(request, 'teachhub/history.html', context)
        else:
            text = '現在、処理中です。しばらくしてから再度、お試しください。'

            return text

    else:
        context = get_history(request, doc_id)
        return render(request, 'teachhub/history.html', context)


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

#############
# その他    #
#############

# wordファイルをpdfファイルに変換


@login_required
def convert_document(request, word_url, pdf_url, lock):
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

        Application.Documents.Open(word_url)
        wdFormatPDF = 17
        print("pdf化開始")
        Application.ActiveDocument.SaveAs2(
            FileName=pdf_url, FileFormat=wdFormatPDF)
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

        # リクエストのnameの情報を変更
        # wordファイルのアップロード先を変更するため
        tmp_name_by_writer = request.FILES['file'].name
        name_by_writer = tmp_name_by_writer.split(".")[0]
        # request.FILES['file'].name = str(request.user.id) + "." \
        #     + "{}_{}_{}".format(textbook_name, chapter_name, section_name) \
        #     + "." + current_time
        request.FILES['file'].name = str(request.user.id) + "." \
            + "{}_{}_{}".format(textbook_name, chapter.id, section.id) \
            + "." + current_time

        form = DocumentForm(request.POST, request.FILES)
        print("request.FILES")
        print(request.FILES)

        doc_info = request.FILES['file'].name
        lst_doc_info = doc_info.split(".")
        print("lst_doc_info")
        print(lst_doc_info)

        p2 = ""
        if form.is_valid():
            form.save()

            user_id = lst_doc_info[0]
            # "{}_{}_{}".format(textbook_name, chapter_name, section_name)の箇所
            section_info = lst_doc_info[1]

            path = 'documents/notes/{0}_{1}/word/{2}.docx'.format(
                user_id, section_info, current_time)

            # TODO
            # パスの変更
            base_word_url = r"C:\Users\kojiy\teachhub\media\documents\{}\{}\word\{}.docx"
            base_pdf_dir = r"C:\Users\kojiy\teachhub\media\documents\{}\{}\pdf"
            # base_word_url = r"C:\Users\tatsu\Documents\teachhub\teachhub\media\documents\{}\{}\word\{}.docx"
            # base_pdf_dir = r"C:\Users\tatsu\Documents\teachhub\teachhub\media\documents\{}\{}\pdf"

            sec_info_by_user = "{0}_{1}".format(user_id, section_info)
            word_url = base_word_url.format(
                category, sec_info_by_user, current_time)
            pdf_url = word_url.replace(
                "word", "pdf").replace(".docx", ".pdf")
            pdf_dir = base_pdf_dir.format(category, sec_info_by_user)
            # pdfを保存するディレクトリの作成
            os.makedirs(pdf_dir, exist_ok=True)

            # データベースの更新
            print("DBの更新")
            document = Document.objects.get(file=path)
            custom_user = CustomUser.objects.get(id=user_id)
            document.custom_user = custom_user
            document.created_at = date
            document.name = name_by_writer
            document.category = category
            document.section_id = section_id
            document.latest = True
            document.save()

            # ファイルのpdf化
            p1 = threading.Thread(target=convert_document, args=(
                request, word_url, pdf_url, lock))
            print("convert_document started")
            p1.start()
            print("started")

            # 1つ前のファイルとの差分作成 / そのファイルの保存
            document_id = document.id
            print("id")
            print(document_id)
            documents = Document.objects.filter(
                custom_user=custom_user, name=name_by_writer, section_id=section_id)
            document_num = documents.count()
            if document_num > 1:
                # id < doc_id
                # nameとuser_idでフィルター
                pre_document = Document.objects.filter(custom_user=custom_user,
                                                       name=name_by_writer, section_id=section_id, id__lt=document_id).order_by('-id').first()

                # データベースの更新
                pre_document.latest = False
                pre_document.save()

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
                # TODO
                # パスの変更
                base_diff_word_url = r"C:\Users\kojiy\teachhub\media\documents\{}\{}\differences\word\{}.docx"
                base_diff_word_dir = r"C:\Users\kojiy\teachhub\media\documents\{}\{}\differences\word"
                # base_diff_word_url = r"C:\Users\tatsu\Documents\teachhub\teachhub\media\documents\{}\{}\differences\word\{}.docx"
                # base_diff_word_dir = r"C:\Users\tatsu\Documents\teachhub\teachhub\media\documents\{}\{}\differences\word"
                diff_word_url = base_diff_word_url.format(
                    category, doc_name, current_time)
                diff_word_dir = base_diff_word_dir.format(category, doc_name)
                diff_pdf_dir = diff_word_dir.replace('word', 'pdf')
                # 差分のwordファイルを保存するディレクトリの作成
                os.makedirs(diff_word_dir, exist_ok=True)
                # 差分のpdfファイルを保存するディレクトリの作成
                os.makedirs(diff_pdf_dir, exist_ok=True)

                document.diff_word_url = diff_word_url
                document.save()

                p2 = threading.Thread(target=compare_documents, args=(
                                      request, pre_word_url, word_url, diff_word_url, lock))

            if p2:
                print("compare_documents started")
                p2.start()

            # urlをDBに格納 update
            print("doc_pdf_url")
            print(pdf_url)
            document.doc_pdf_url = pdf_url
            document.save()
            p1.join()
            print("終了")

            return redirect(reverse('teachhub:document_note', args=(section_id,)))
    else:
        print("カテゴリー")
        print(category)
        print(section_id)
        documents = Document.objects.filter(
            category=category, section_id=section_id, latest=True).order_by('id')
        print("document")
        print(documents)
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

# 履歴情報の取得


@login_required
def get_history(request, doc_id):
    user = request.user
    print(user)
    document = Document.objects.get(id=doc_id)
    section = document.section
    documents = Document.objects.filter(
        custom_user=user, section=section).order_by('-id')
    histories = documents.values(
        'id', 'doc_pdf_url', 'diff_word_url', 'created_at', 'custom_user')
    lst_histories = list(histories)
    context = {'lst_histories': lst_histories}

    return context

# 取得した履歴情報をテンプレートにレンダリングする


@login_required
def render_history(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    pdf_url = document.doc_pdf_url
    context = context_to_show_pdf(document, pdf_url)
    context_histories = get_history(request, doc_id)
    context.update(context_histories)

    return render(request, 'teachhub/history.html', context)


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
def update_document(request, doc_id):
    # ↓ データベースから与えられたid番号を取得(if文の外に書く)
    document = get_object_or_404(Document, id=doc_id)  # /documents/4/update
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
# TODO
# ファイルも削除
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    section = document.section
    section_id = section.id
    if request.method == 'GET':
        return render(
            request,
            'teachhub/document_confirm_delete.html',
            dict(document=document)
        )
    elif request.method == 'POST':
        document.delete()
        # return rediredt('/documents/')
        return redirect(reverse('teachhub:document_note', args=(section_id,)))
