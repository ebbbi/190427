from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^weather/$', views.weather, name="weather"),
    url(r'^join/$', views.signup, name='join'),
    url(r'^join_fail/$', views.join_fail, name='join_fail'),
    url(r'^join_fail2/$', views.join_fail2, name='join_fail2'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^logout/$', views.signout, name='logout'),
    url(r'^images/$', views.images, name='images'),
    url(r'^news/$', views.new, name="new"),
    url(r'^post/(?P<index>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<index>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^comment/(?P<index>\d+)/delete/(?P<cindex>\d+)/$', views.comment_delete, name="comment_delete"),
    url(r'^comment/(?P<index>\d+)/edit/(?P<cindex>\d+)/$', views.comment_edit, name="comment_edit"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)