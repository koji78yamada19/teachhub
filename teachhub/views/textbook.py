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
        context = {"textbooks": textbooks, "subject_id": subject_id}
        return render(
            request,
            'teachhub/textbook_list.html',
            context
        )


# from django.shortcuts import render
# from django.views import generic
# from teachhub.models import Textbook
# from django.contrib.auth.mixins import LoginRequiredMixin

# # 教科書一覧ビュー


# class TextbookListView(LoginRequiredMixin, generic.ListView):

#     queryset = Textbook.objects.all()


# textbook_list = TextbookListView.as_view()
