# -*-coding:utf-8-*-
from django.urls import path

from Knowledge_base.search import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_advanced', views.search_advanced, name='search_advanced'),
    path('search_general', views.search_general, name='search_general'),
    path('get_paper_by_id', views.get_paper_by_id, name='get_paper_by_id'),
    path('get_fos_agg', views.get_fos_agg, name='get_fos_agg'),
    path('download', views.download, name='download')
]

