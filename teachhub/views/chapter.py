from django.shortcuts import render
from teachhub.models import Chapter, Textbook, Subject
from django.contrib.auth.decorators import login_required

# textbook_idでフィルタリングした章一覧ビュー


@login_required
def chapter_list(request, subject_id, textbook_id):
    if request.method == 'GET':
        chapter_list = Chapter.objects.filter(
            textbook_id=textbook_id).order_by('id')
        textbook = Textbook.objects.get(id=textbook_id)
        subject_name = Subject.objects.get(id=subject_id).name.split('-')[1]
        context = {
            "chapter_list": chapter_list,
            "textbook": textbook,
            "subject_id": subject_id,
            "subject_name": subject_name
        }
        return render(
            request,
            'teachhub/chapter_list.html',
            context
        )
