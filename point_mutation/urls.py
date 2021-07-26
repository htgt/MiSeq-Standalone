from django.urls import path
from point_mutation import views


app_name = 'point_mutation'
urlpatterns = [
    path('', views.home, name="home"),
    path('point_mutation', views.point_mutation_upload, name='upload'),
    path('point_mutation_view', views.point_mutation_view, name='view'),
    path('point_mutation_allele/<miseq>/<oligo_index>/<exp>', views.point_mutation_allele, name='allele')
]
