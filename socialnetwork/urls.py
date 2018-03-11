from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views
from socialnetwork import views as my_views

urlpatterns = [
    url(r'^$',              views.search,           name='home'),
    url(r'^search$',        views.search,           name='search'),
    url(r'^my_profile$',    views.my_profile,       name='my_profile'),
    url(r'^other_profile$', views.other_profile,    name='other_profile'),
    url(r'^follow$',        views.follow,           name='follow'),
    url(r'^unfollow$',      views.unfollow,         name='unfollow'),
    url(r'^follow_stream$', views.follow_stream,    name='follow_stream'),
    url(r'^create$',        views.create,           name='create'),
    # url(r'^comment$',       views.comment,          name='comment'),
    url(r'^add-comment/(?P<post_id>\d+)$',   views.add_comment,      name='add_comment'),
    url(r'^get-list-json$', views.get_list_json),
    # url(r'^get-list-json-comment$', views.get_list_json_comment),
    url(r'^register$',      views.register,         name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    # url(r'^add-item$', views.add_profile, name='add'),
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9]+)/(?P<token>[a-z0-9\-]+)$',
        my_views.confirm_registration, name='confirm'),
]

