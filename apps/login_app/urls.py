from django.conf.urls import url
from . import views
                    
urlpatterns = [
 url(r'^$', views.index),
 url(r'^register$', views.add_new_user),
 url(r'^login$', views.login_user),
 url(r'^wall$',views.display_wall),
 url(r'^post$',views.post_message),
 url(r'^logout$',views.logout_user),
 url(r'^comment$',views.post_comment),
 url(r'^delete$', views.delete_msg),
]