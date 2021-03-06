from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^upload/(?P<filename>[^/]+)$',
        views.FileUploadView.as_view(),
        name='file-upload'),
    url(r'^upload/$',
        views.FileUploadView.as_view(),
        name='file-upload-POST'),
    url(r'^keywords/$',
        views.FileUploadViewKeywords.as_view(),
        name='keywords-upload'),
    url(r'^keywords/(?P<pk>[0-9]+)/$',
        views.KeywordDetail.as_view(),
        name='keywords-get-delete'),
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),
])
