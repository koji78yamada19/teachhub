from django.urls import path
from teachhub import views

app_name = 'teachhub'  # URL逆引用

urlpatterns = [
    path('textbooks/', views.textbook_list, name='textbook_list'),
    path('textbooks/<int:textbook_id>/chapters/',
         views.chapter_list, name='chapter_list'),
    path('textbooks/chapters/sections/<int:section_id>/notes/',
         views.document_note, name='document_note'),
#     path('textbooks/chapters/sections/<int:section_id>/note/history/',
#          views.get_history, name='history'),
    path('textbooks/chapters/sections/<int:section_id>/tests/',
         views.document_test, name='document_test'),
    path('documents/convert/', views.convert_document, name='convert'),
    path('documents/compare/', views.compare_documents, name='compare'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),
    path('documents/<pk>/update/', views.update_document, name='update_document'),
#     path('documents/<pk>/delete/', views.document_delete, name='document_delete'),
    path('documents/<int:doc_id>/delete/', views.delete_document, name='delete_document'),
    # path('documents/<int:doc_id>/history/', views.render_history, name='render_history'),
    # path('documents/history/<int:doc_id>/', views.show_history_detail, name='history_detail'),
    # path('documents/<int:doc_id>/diff/', views.show_diff, name='diff')
]
