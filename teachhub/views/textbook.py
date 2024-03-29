from django.shortcuts import render
from teachhub.models import Textbook, Subject
from django.contrib.auth.decorators import login_required

# textbook_idでフィルタリングした章一覧ビュー


@login_required
def textbook_list(request, subject_id):
    if request.method == 'GET':
        subject = Subject.objects.get(id=subject_id)
        textbooks = Textbook.objects.filter(
            subject=subject).order_by('id')
        context = {"textbooks": textbooks, "subject": subject}
        return render(
            request,
            'teachhub/textbook_list.html',
            context
        )
