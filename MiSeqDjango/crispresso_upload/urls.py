from django.conf.urls import url
from crispresso_upload import views

urlpatterns = [
    url(r'^api/crispresso-upload$', views.crispresso_upload),
    url(r'^api/crispresso-upload/(?P<pk>[0-9]+)$', views.crispresso_detail),
    url(r'^api/crispresso-upload/published$', views.crispresso_list_published)
]