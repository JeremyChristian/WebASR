from django.conf.urls import url
from frontend import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = format_suffix_patterns([
	url(r'^$', views.api_root),
     url(r'^uploads$',
        views.UploadList.as_view(),
        name='uploads'),
    url(r'^upload/(?P<pk>[0-9]+)/$',
        views.UploadDetail.as_view(),
        name='upload'),
    url(r'^newupload$',
        views.UploadCreate.as_view(),
        name='newupload'),
    url(r'^systems$',
        views.SystemList.as_view(),
        name='systems'),
    url(r'^system/(?P<pk>[0-9]+)/$',
        views.SystemDetail.as_view(),
        name='system'),
    url(r'^users$',
        views.UserList.as_view(),
        name='users'),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user'),
    url(r'^signup',
        views.UserCreate.as_view(),
        name='signup'),
    url(r'^api-auth/', 
    	include('rest_framework.urls',
		namespace='rest_framework')),
])

# urlpatterns = [
#     url(r'^uploads/$', views.upload_list),
#     url(r'^uploads/(?P<pk>[0-9]+)/$', views.upload_detail),
#     url(r'^systems/$', views.system_list),
#     url(r'^systems/(?P<pk>[0-9]+)/$', views.system_detail),
# ]

