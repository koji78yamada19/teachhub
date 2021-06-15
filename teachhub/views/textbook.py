from django.shortcuts import render
from django.views import generic
from teachhub.models import Textbook
from django.contrib.auth.mixins import LoginRequiredMixin

# 教科書一覧ビュー


class TextbookListView(LoginRequiredMixin, generic.ListView):

    queryset = Textbook.objects.all()


textbook_list = TextbookListView.as_view()
