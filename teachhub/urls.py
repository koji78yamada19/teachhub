from django.urls import path
from teachhub import views

app_name = 'teachhub'  # URL逆引用

urlpatterns = [
    path('documents/', views.document_list, name='document_list'),
    path('notes/<int:section_id>/', views.document_note, name='document_note'),
    path('tests/<int:section_id>/', views.document_test, name='document_test'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),
    path('documents/<pk>/update/', views.document_update, name='document_update'),
    path('documents/<pk>/delete/', views.document_delete, name='document_delete'),

    # path('<int:chapter_id>/sections/', views.section_list, name='section_list'),
    path('<int:textbook_id>/chapters/', views.chapter_list, name='chapter_list'),
    path('textbooks/', views.textbook_list, name='textbook_list')
]
