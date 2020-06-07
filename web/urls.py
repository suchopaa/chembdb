from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import ReceptorDetail, receptor_detail, activity_detail, ligand_detail, source_detail 

urlpatterns = [
	path('', views.search, name='web-search'),
	path('activity/', views.activity, name='web-activity'),
	path('receptor/', views.receptor, name='web-receptor'),
	path('about/', views.about, name='web-about'),
	path('search_help/', views.search_help, name='web-search_help'),
	path('activity_list_help/', views.activity_list_help, name='web-activity_list_help'),
	path('activity_detail_help/', views.activity_detail_help, name='web-activity_detail_help'),
	path('receptor_list_help/', views.receptor_list_help, name='web-receptor_list_help'),
	path('receptor_detail_help/', views.receptor_detail_help, name='web-receptor_detail_help'),
	path('ligand_detail_help/', views.ligand_detail_help, name='web-ligand_detail_help'),
	path('source_detail_help/', views.source_detail_help, name='web-source_detail_help'),
	path('ketcher/', views.ketcher, name='web-ketcher'),
	path('export/', views.export, name='web-export'),
	path('export_selected/', views.export_selected, name='web-export-selected'),
	url(r'^receptor/(?P<receptor_id>[-\w]+)', receptor_detail, name='web-receptor-detail'),
	url(r'^activity/(?P<activity_id>[-\w]+)', activity_detail, name='web-activity-detail'),
	url(r'^ligand/(?P<ligand_id>[-\w]+)', ligand_detail, name='web-ligand-detail'),
	url(r'^source/(?P<source_id>[-\w]+)', source_detail, name='web-source-detail')
]

urlpatterns += staticfiles_urlpatterns()
