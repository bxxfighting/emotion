from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView()),
    url(r'^user/mod/list/$', views.ListUserModView()),
    url(r'^password/change/$', views.ChangePasswordView()),
    # role
    url(r'^role/list/$', views.ListRoleView()),
    url(r'^role/create/$', views.CreateRoleView()),
    url(r'^role/update/$', views.UpdateRoleView()),
    url(r'^role/delete/$', views.DeleteRoleView()),
    url(r'^role/mods/set/$', views.SetRoleModsView()),
    # mod
    url(r'^mod/list/$', views.ListModView()),
    url(r'^mod/create/$', views.CreateModView()),
    url(r'^mod/update/$', views.UpdateModView()),
    url(r'^mod/delete/$', views.DeleteModView()),
    # user
    url(r'^user/list/$', views.ListUserView()),
    url(r'^user/create/$', views.CreateUserView()),
    url(r'^user/update/$', views.UpdateUserView()),
    url(r'^user/delete/$', views.DeleteUserView()),
    # url
    url(r'^url/list/$', views.ListUrlView()),
    url(r'^url/create/$', views.CreateUrlView()),
    url(r'^url/update/$', views.UpdateUrlView()),
    url(r'^url/delete/$', views.DeleteUrlView()),
]
