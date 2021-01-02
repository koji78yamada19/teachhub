from django.urls import path
from teachhub import views

app_name = 'teachhub'  # URL逆引用

urlpatterns = [
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),
    path('documents/<pk>/update/', views.document_update, name='document_update'),
    path('documents/<pk>/delete/', views.document_delete, name='document_delete'),

    path('chapters/', views.chapter_list, name='chapter_list'),

]