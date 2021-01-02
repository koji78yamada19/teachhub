from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from teachhub.models import Chapter

class ChapterListView(generic.ListView):
    queryset = Chapter.objects.all()

chapter_list = ChapterListView.as_view()