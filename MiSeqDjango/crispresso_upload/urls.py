from django.conf.urls import url
from crispresso_upload import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^api/crispresso-upload$', views.crispresso_upload)
]