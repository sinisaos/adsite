from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.question_list, name='question_list'),
    # url(r'^$', views.QuestionListView.as_view(), name='question_list'),
    url(r'^unsolved/$', views.unsolved_list, name='unsolved_list'),
    url(r'^solved/$', views.solved_list, name='solved_list'),
    url(r'^ask/$', views.question_ask, name='question_ask'),
    url(r'^tagged/(?P<tag_slug>[\w-]+)/$', views.tagged, name='tagged'),
    url(r'^(?P<slug>[\w-]+)/delete/$',
        views.question_delete, name='question_delete'),
    url(r'^(?P<slug>[\w-]+)/edit/$',
        views.question_update, name='question_update'),
    url(r'^(?P<slug>[\w-]+)/answer/(?P<pk>\d+)/edit/$',
        views.answer_update, name='answer_update'),
    url(r'^(?P<slug>[\w-]+)/answer/(?P<pk>\d+)/delete/$',
        views.answer_delete, name='answer_delete'),
    url(r'^(?P<slug>[\w-]+)/$', views.question_detail,
        name='question_detail'),
    url(r'^(?P<slug>[\w-]+)/like/$', views.QuestionLikeToggle.as_view(),
        name='like-toggle'),
    url(r'^(?P<slug>[\w-]+)/like/(?P<pk>\d+)/$',
        views.answer_likes,
        name='answer_likes'),
    url(r'^(?P<slug>[\w-]+)/dislike/(?P<pk>\d+)/$',
        views.answer_dislikes,
        name='answer_dislikes'),
    url(r'^(?P<slug>[\w-]+)/accept/$', views.accept, name='accept'),
]
