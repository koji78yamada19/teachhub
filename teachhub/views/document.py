from django.db import reset_queries
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse  # function の中で書くとき（評価タイミングの違い）
from django.contrib.auth.decorators import login_required

from teachhub.models import Textbook, Chapter, Section, Document
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
def document_detail(request, pk):
    # def get_document(request, pk):
    # 教材の詳細を表示(pdfとして表示)
    if request.method == 'GET':
        document = get_object_or_404(Document, pk=pk)
        path = document.path
        url = 'https://prod-22.japanwest.logic.azure.com:443/workflows/e549f57770b24d1f8255ccb2ab1fc8fb/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=VTVnuk1nJXTihBEMQl25PRcjBrOaqbYu7u1h9kTBrqQ'
        data = {'Path': path}

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
def upload_and_get_document(request, section_id):
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
    subject_name = '日本史'

    if request.method == 'GET':
        documents = Document.objects.filter(
            category=category, section_id=section_id).order_by('id')
        context = {
            "documents": documents,
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
        title = f'{document_name}'
        path = f'/documents/{subject_name}/{textbook_name}/{chapter_name}_{section_name}/{category_in_path}/user_{user_id}'

        url = 'https://prod-17.japanwest.logic.azure.com:443/workflows/aa397302f6694e959fca72dbab910124/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=g3Lk7aJOmOEkAWksX_5rcZjCTHIMNo0OShp8pLHYsnw'
        files = {'file': (title, f, 'multipart/form-data')}
        data = {
            'Title': title,
            'Path': path
        }

        res = requests.post(url, files=files, data=data)
        print('res')
        print(res.text)
        JST = timezone(timedelta(hours=+9), 'JST')
        date = datetime.now(JST)
        # current_time = date.strftime('%Y-%m-%d-%H-%M-%S')

        # データベースの更新
        print("DBの更新")
        custom_user = CustomUser.objects.get(id=user_id)
        try:
            document = Document.objects.get(
                category=category, section_id=section_id, custom_user=custom_user)
            document.updated_by = date
            document.updated_at = custom_user
        except:
            document = Document(
                textbook=textbook,
                chapter=chapter,
                section=section,
                name=document_name.split('.')[0],
                path=f'{path}/{title}',
                content='',
                category=category,
                custom_user=custom_user,
                updated_by=custom_user,
                updated_at=date,
                created_by=custom_user,
                created_at=date
            )
        document.save()

        if category == '板書案':
            revers_url = 'teachhub:document_note'
        elif category == '小テスト':
            revers_url = 'teachhub:document_test'

        return redirect(reverse(revers_url, args=(section_id,)))


###############
# Delete 削除 #
###############
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    section = document.section
    section_id = section.id
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
        data = {'Path': path}
        requests.post(url, data=data)
        document.delete()
        return redirect(reverse('teachhub:document_note', args=(section_id,)))


def download_document(request, doc_id):
    print('doc')
    print(doc_id)
    document = get_object_or_404(Document, id=doc_id)
    path = document.path
    print("path")
    print(path)

    url = 'https://prod-01.japanwest.logic.azure.com:443/workflows/471d46fc40cc4a64a3abe71adbec1fa9/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=z0FgPb_kOXJudulNY3fyAm1Qkzcnkwd8xN5B7ebAdBI'
    data = {'Path': path}
    res = requests.post(url, data=data)
    print(type(res.content))

    document_name = document.name
    f = open(f'{document_name}.docx', mode='wb+')
    f.write(res.content)
    f.seek(0)
    f.close

    return FileResponse(f)


##################
# ログイン後の画面 #
##################
def root_to_login(request):
    return redirect('textbooks/')

# 履歴詳細表示

# @login_required
# def show_history_detail(request, doc_id):
#     document = get_object_or_404(Document, id=doc_id)
#     pdf_url = document.doc_pdf_url

#     context = context_to_show_pdf(document, pdf_url)
#     # 履歴の情報をコンテクストに追加
#     context_histories = get_history(request, doc_id)
#     context.update(context_histories)

#     return render(request, 'teachhub/history.html', context)

# # 差分詳細表示


# @login_required
# def show_diff(request, doc_id):
#     document = get_object_or_404(Document, id=doc_id)
#     diff_word_url = document.diff_word_url
#     diff_pdf_url = document.diff_pdf_url

#     # 既にpdfがある場合
#     if diff_pdf_url:
#         pdf_url = diff_pdf_url

#         context = context_to_show_pdf(document, pdf_url)
#         context_histories = get_history(request, doc_id)
#         context.update(context_histories)

#         return render(request, 'teachhub/history.html', context)

#     # 差分のwordファイルがある場合
#     elif diff_word_url:
#         if os.path.isfile(diff_word_url):
#             lock = threading.Lock()
#             diff_pdf_url = diff_word_url.replace(
#                 "word", "pdf").replace(".docx", ".pdf")
#             convert_document(request, diff_word_url, diff_pdf_url, lock)
#             document.diff_pdf_url = diff_pdf_url
#             document.save()
#             pdf_url = diff_pdf_url

#             context = context_to_show_pdf(document, pdf_url)
#             context_histories = get_history(request, doc_id)
#             context.update(context_histories)

#             return render(request, 'teachhub/history.html', context)
#         else:
#             text = '現在、処理中です。しばらくしてから再度、お試しください。'

#             return text

#     else:
#         context = get_history(request, doc_id)
#         return render(request, 'teachhub/history.html', context)


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
# その他    #
#############

# wordファイルをpdfファイルに変換


# @login_required
# def convert_document(request, word_url, pdf_url, lock):
#     with lock:
#         # Wordを起動する前にこれを呼び出す
#         pythoncom.CoInitialize()
#         # #Wordを起動する : Applicationオブジェクトを生成する
#         try:
#             Application = win32com.client.gencache.EnsureDispatch(
#                 "Word.Application")
#         except AttributeError:
#             # Remove cache and try again.
#             MODULE_LIST = [m.__name__ for m in sys.modules.values()]
#             for module in MODULE_LIST:
#                 if re.match(r'win32com\.gen_py\..+', module):
#                     del sys.modules[module]
#             shutil.rmtree(os.path.join(os.environ.get(
#                 'LOCALAPPDATA'), 'Temp', 'gen_py'))
#             Application = win32com.client.gencache.EnsureDispatch(
#                 "Word.Application")

#         Application.Documents.Open(word_url)
#         wdFormatPDF = 17
#         print("pdf化開始")
#         Application.ActiveDocument.SaveAs2(
#             FileName=pdf_url, FileFormat=wdFormatPDF)
#         print("pdf化終了")

#         Application.ActiveDocument.Close()
#         #Wordを終了する : Quitメソッドを呼ぶ
#         Application.Quit()
#         pythoncom.CoUninitialize()

#     return ""


# # wordファイルの差分を取る
# @login_required
# def compare_documents(request, original_doc, revised_doc, diff_word_url, lock):
#     with lock:
#         pythoncom.CoInitialize()
#         try:
#             Application = win32com.client.gencache.EnsureDispatch(
#                 "Word.Application")
#         except AttributeError:
#             MODULE_LIST = [m.__name__ for m in sys.modules.values()]
#             for module in MODULE_LIST:
#                 if re.match(r'win32com\.gen_py\..+', module):
#                     del sys.modules[module]
#             shutil.rmtree(os.path.join(os.environ.get(
#                 'LOCALAPPDATA'), 'Temp', 'gen_py'))
#             Application = win32com.client.gencache.EnsureDispatch(
#                 "Word.Application")

#         ori_doc_open = Application.Documents.Open(original_doc)
#         rev_doc_open = Application.Documents.Open(revised_doc)
#         print("差分計算開始")
#         Application.CompareDocuments(ori_doc_open, rev_doc_open)
#         Application.ActiveDocument.SaveAs2(FileName=diff_word_url)
#         print("差分計算終了")

#         Application.ActiveDocument.Close()
#         Application.Quit()
#         pythoncom.CoUninitialize()

#     return ""


# 履歴情報の取得


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

# # 取得した履歴情報をテンプレートにレンダリングする


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
