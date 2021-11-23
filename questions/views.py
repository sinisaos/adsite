from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import RedirectView
from taggit.models import Tag

from .forms import AnswerForm, QuestionForm
from .models import Answer, Question

User = get_user_model()


def question_list(request):
    rank_users = (
        User.objects.filter(answer__is_accepted=True)
        .annotate(num_answer=Count("answer"))
        .order_by("-num_answer")
    )
    queryset = Question.objects.all()

    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(Q(qus__icontains=query)).distinct()

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    context = {"questions": query_list, "rank_users": rank_users}
    return render(request, "questions/question_list.html", context)


def unsolved_list(request):
    queryset = Question.objects.filter(has_accepted_answer=False)
    rank_users = (
        User.objects.filter(answer__is_accepted=True)
        .annotate(num_answer=Count("answer"))
        .order_by("-num_answer")
    )

    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(Q(qus__icontains=query)).distinct()

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    context = {"questions": query_list, "rank_users": rank_users}
    return render(request, "questions/question_list.html", context)


def solved_list(request):
    queryset = Question.objects.filter(has_accepted_answer=True)
    rank_users = (
        User.objects.filter(answer__is_accepted=True)
        .annotate(num_answer=Count("answer"))
        .order_by("-num_answer")
    )

    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(Q(qus__icontains=query)).distinct()

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    context = {"questions": query_list, "rank_users": rank_users}
    return render(request, "questions/question_list.html", context)


def question_detail(request, slug=None):
    question = get_object_or_404(Question, slug=slug)
    session_key = "viewed_question_{}".format(question.pk)
    if not request.session.get(session_key, False):
        question.views += 1
        question.save()
        request.session[session_key] = True
    answers_list = Answer.objects.filter(question=question)
    count = Answer.objects.filter(question=question).count()
    context = {
        "question": question,
        "answers_list": answers_list,
        "count": count,
    }
    if request.user.is_authenticated:
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            messages.success(request, "Answer was Posted.")
            form = AnswerForm()
            return redirect(question.get_absolute_url())
        context = {
            "question": question,
            "form": form,
            "answers_list": answers_list,
            "count": count,
        }
    return render(request, "questions/question_detail.html", context)


class QuestionLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Question, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


@login_required()
def answer_likes(request, slug=None, pk=None):
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, pk=pk)
    user = request.user
    session_key = "viewed_answer_{}".format(answer.pk)
    if not request.session.get(session_key, False) and user.is_authenticated():
        answer.likes += 1
        answer.save(update_fields=["likes"])
        request.session[session_key] = True
    return redirect(question.get_absolute_url())


@login_required()
def answer_dislikes(request, slug=None, pk=None):
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, pk=pk)
    user = request.user
    session_key = "viewed_answer_{}".format(answer.pk)
    if not request.session.get(session_key, False) and user.is_authenticated():
        answer.dislikes += 1
        answer.save(update_fields=["dislikes"])
        request.session[session_key] = True
    return redirect(question.get_absolute_url())


@login_required
def accept(request, slug=None):
    question = get_object_or_404(Question, slug=slug)
    answers = Answer.objects.filter(question=question)
    for answer in answers:
        answer.is_accepted = False
        answer.save(update_fields=["is_accepted"])
    answer.is_accepted = True
    answer.save(update_fields=["is_accepted"])
    messages.info(request, "Answer accepted.")
    question.has_accepted_answer = True
    question.save(update_fields=["has_accepted_answer"])

    return redirect(question.get_absolute_url())


"""
@login_required
@ajax_required
def accept(request, slug=None):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    user = request.user

    if answer.question.user == user:
        answer.accept()
        return HttpResponse()

    else:
        return HttpResponseForbidden()
"""


def tagged(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    questions_list = Question.objects.filter(tags=tag)

    paginator = Paginator(questions_list, 10)

    page = request.GET.get("page")

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = {"questions": questions, "tag": tag}
    return render(request, "questions/tagged.html", context)


@login_required()
def question_ask(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        form.save_m2m()
        messages.info(request, "Question was Posted.")
        return redirect("questions:question_list")
    context = {"form": form, "title": "Ask Question"}
    return render(request, "questions/ask.html", context)


@login_required()
def question_update(request, slug=None):
    instance = get_object_or_404(Question, slug=slug)
    form = QuestionForm(request.POST or None, instance=instance)
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        form.save_m2m()
        messages.info(request, "Question was Updated.")
        return redirect(question.get_absolute_url())
    context = {"form": form, "title": "Edit Question"}
    return render(request, "questions/ask.html", context)


@login_required()
def question_delete(request, slug=None):
    question = get_object_or_404(Question, slug=slug)
    if question.user == request.user:
        question.delete()
        messages.info(request, "Question was Deleted.")
        return redirect("questions:question_list")


@login_required()
def answer_update(request, slug=None, pk=None):
    question = get_object_or_404(Question, slug=slug)
    instance = get_object_or_404(Answer, pk=pk)
    form = AnswerForm(request.POST or None, instance=instance)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.user = request.user
        answer.question = question
        answer.save()
        messages.info(request, "Answer was Updated.")
        return redirect(question.get_absolute_url())
    context = {"form": form, "title": "Update Answer"}
    return render(request, "questions/answer.html", context)


@login_required()
def answer_delete(request, slug=None, pk=None):
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, pk=pk)

    if answer.user == request.user:
        answer.delete()
        messages.info(request, "Answer was Deleted.")
        return redirect(question.get_absolute_url())
