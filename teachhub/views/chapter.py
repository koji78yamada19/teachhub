from django.shortcuts import render
from teachhub.models import Chapter, Textbook
from django.contrib.auth.decorators import login_required

# textbook_idでフィルタリングした章一覧ビュー


@login_required
def chapter_list(request, subject_id, textbook_id):
    if request.method == 'GET':
        chapter_list = Chapter.objects.filter(
            textbook_id=textbook_id).order_by('id')
        textbook = Textbook.objects.get(id=textbook_id)
        context = {
            "chapter_list": chapter_list,
            "textbook": textbook,
            "subject_id": subject_id
        }
        return render(
            request,
            'teachhub/chapter_list.html',
            context
        )
