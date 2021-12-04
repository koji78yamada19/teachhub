from django.urls import path
from teachhub import views

app_name = 'teachhub'  # URL逆引用

urlpatterns = [
    path('',
         views.get_subject_areas, name='subject_areas'),
    #     path('subject-areas/',
    #          views.get_subject_areas, name='subject_areas'),
    path('classifications/<int:classification_id>/subject-areas/<int:area_id>/subjects/',
         views.get_subjects, name='subjects'),
    path('subjects/<int:subject_id>/textbooks/',
         views.textbook_list, name='textbook_list'),
    path('subjects/<int:subject_id>/textbooks/<int:textbook_id>/chapters/sections',
         views.chapter_list, name='chapter_list'),
    path('subjects/<int:subject_id>/textbooks/<int:textbook_id>/chapters/sections/<int:section_id>/notes/',
         views.upload_and_get_documents, name='document_note'),
    path('subjects/<int:subject_id>/textbooks/<int:textbook_id>/chapters/sections/<int:section_id>/tests/',
         views.upload_and_get_documents, name='document_test'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<pk>/', views.get_document, name='get_document'),
    path('documents/<int:doc_id>/delete/',
         views.delete_document, name='delete_document'),
    path('documents/<int:doc_id>/download/',
         views.download_document, name='download'),
]
