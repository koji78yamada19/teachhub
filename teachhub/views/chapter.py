from django.shortcuts import render
from teachhub.models import Chapter, Textbook

# textbook_idでフィルタリングした章一覧ビュー
def chapter_list(request, textbook_id):
    chapter = "chapters"
    if request.method == 'GET':
        chapter_list = Chapter.objects.filter(textbook_id=textbook_id).order_by('id')             
        text = Textbook.objects.get(id=textbook_id)
        text_name = text.name      
        # 下記でもnameをとれる
        # chapter = chapter_list.first()
        # text_name = chapter.textbook.name
        context = {"chapter_list":chapter_list, "text_name":text_name}
        return render(
            request,
            'teachhub/chapter_list.html', 
            context
        )