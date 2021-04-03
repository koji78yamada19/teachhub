from django.urls import path
from teachhub import views

app_name = 'teachhub'  # URL逆引用

urlpatterns = [
    path('textbooks/', views.textbook_list, name='textbook_list'),
    path('textbooks/<int:textbook_id>/chapters/', views.chapter_list, name='chapter_list'),
    path('textbooks/chapters/sections/<int:section_id>/notes/', views.document_note, name='document_note'),
    path('textbooks/chapters/sections/<int:section_id>/tests/', views.document_test, name='document_test'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),
    path('documents/<pk>/update/', views.document_update, name='document_update'),
    path('documents/<pk>/delete/', views.document_delete, name='document_delete'),

]