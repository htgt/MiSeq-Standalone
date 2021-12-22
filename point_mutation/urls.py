from django.urls import path
from point_mutation import views


app_name = 'point_mutation'
urlpatterns = [
    path('', views.home, name="home"),
    path('point_mutation', views.point_mutation_upload, name='upload'),
    path('point_mutation_upload', views.point_mutation_upload_folder, name='upload_folder'),
    path('point_mutation_folder_upload', views.folder_upload_ajax, name='ajax_upload'),
    path('point_mutation_view', views.point_mutation_view, name='view'),
    path('point_mutation_allele/<miseq>/<oligo_index>/<exp>', views.point_mutation_allele, name='allele'),
    path('point_mutation_summary/<miseq>/<oligo_index>/<exp>/<limit>', views.allele_summary, name='summary'),
    path('point_mutation/summary', views.allele_summary_ajax, name='summary_test')
]
