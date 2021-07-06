from django.urls import path
from teachhub import views

app_name = 'teachhub'  # URL逆引用

urlpatterns = [
    path('', views.root_to_login, name='redirect'),
    path('textbooks/', views.textbook_list, name='textbook_list'),
    path('textbooks/<int:textbook_id>/chapters/sections',
         views.chapter_list, name='chapter_list'),
    path('textbooks/chapters/sections/<int:section_id>/notes/',
         views.upload_and_get_document, name='document_note'),
    path('textbooks/chapters/sections/<int:section_id>/tests/',
         views.upload_and_get_document, name='document_test'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:doc_id>/delete/',
         views.delete_document, name='delete_document'),
    path('documents/<int:doc_id>/download/',
         views.download_document, name='download'),
    #     path('documents/convert/', views.convert_document, name='convert'),
    #     path('documents/compare/', views.compare_documents, name='compare'),
    #     path('documents/<int:doc_id>/history/',
    #          views.render_history, name='render_history'),
    #     path('documents/history/<int:doc_id>/',
    #          views.show_history_detail, name='history_detail'),
    #     path('documents/<int:doc_id>/diff/', views.show_diff, name='diff')
]
