from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.question_list, name="question_list"),
    re_path(r"^unsolved/$", views.unsolved_list, name="unsolved_list"),
    re_path(r"^solved/$", views.solved_list, name="solved_list"),
    re_path(r"^ask/$", views.question_ask, name="question_ask"),
    re_path(r"^tagged/(?P<tag_slug>[\w-]+)/$", views.tagged, name="tagged"),
    re_path(
        r"^(?P<slug>[\w-]+)/delete/$",
        views.question_delete,
        name="question_delete",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/edit/$",
        views.question_update,
        name="question_update",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/answer/(?P<pk>\d+)/edit/$",
        views.answer_update,
        name="answer_update",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/answer/(?P<pk>\d+)/delete/$",
        views.answer_delete,
        name="answer_delete",
    ),
    re_path(r"^(?P<slug>[\w-]+)/$", views.question_detail, name="question_detail"),
    re_path(
        r"^(?P<slug>[\w-]+)/like/$",
        views.QuestionLikeToggle.as_view(),
        name="like-toggle",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/like/(?P<pk>\d+)/$",
        views.answer_likes,
        name="answer_likes",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/dislike/(?P<pk>\d+)/$",
        views.answer_dislikes,
        name="answer_dislikes",
    ),
    re_path(r"^(?P<slug>[\w-]+)/accept/$", views.accept, name="accept"),
]
