# from django.shortcuts import render
# from teachhub.models import Section, Chapter

# # chapter_idでフィルタリングした章一覧ビュー
# def section_list(request, chapter_id):
#     section = "sections"
#     if request.method == 'GET':
#         section_list = Section.objects.filter(chapter_id=chapter_id).order_by('id')      
#         chapter=Chapter.objects.get(id=chapter_id)
#         chapter_name=chapter.name
#         # section = section_list.first()
#         # chapter_name = section.chapter.name         
#         context = {"section_list":section_list, "chapter_name":chapter_name}
#         return render(
#             request,
#             'teachhub/section_list.html', 
#             context
#         )