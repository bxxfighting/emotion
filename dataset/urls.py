from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^comment/list/$', views.ListCommentView()),
    url(r'^comment/update/$', views.UpdateCommentView()),
    url(r'^comment/check/$', views.CheckCommentView()),
    url(r'^stopword/list/$', views.ListStopwordView()),
    url(r'^stopword/create/$', views.CreateStopwordView()),
    url(r'^stopword/update/$', views.UpdateStopwordView()),
    url(r'^stopword/delete/$', views.DeleteStopwordView()),
]
