from django.urls import path
from teachhub import views

# app_name = 'stores'  # URL逆引用

urlpatterns = [
    path('documents/', views.document_list, name='document_list'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),

]