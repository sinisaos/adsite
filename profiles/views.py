from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# from django.db import transaction
from django.contrib import messages
from django.views.generic.edit import DeleteView
from questions.models import Question, Answer
from ads.models import Ad
from .forms import ProfileForm


User = get_user_model()


def user_profile(request, pk, username):
    user = get_object_or_404(User, pk=pk)
    username = get_object_or_404(User, username=username)
    questions = Question.objects.filter(user=user.pk)
    question = Question.objects.filter(user=user).count()
    ads = Ad.objects.filter(user=user.pk)
    ad_count = Ad.objects.filter(user=user).count()
    answer = Answer.objects.filter(user=user).count()
    accepted_answer = Answer.objects.filter(
        user=user, is_accepted=True).count()

    context = {'user_profile': user,
               'question': question,
               'answer': answer,
               'accepted_answer': accepted_answer,
               'questions': questions,
               'ads': ads,
               'ad_count': ad_count}

    return render(request, 'user_profile.html', context)


@login_required
# @transaction.atomic
def update_profile(request, pk, username):
    # user = User.objects.get(pk=pk)
    username = get_object_or_404(User, username=username)
    if request.method == 'POST':
        # user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        # if user_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            messages.success(request,
                             ('Your profile was successfully updated!'))
            return redirect('profiles:profile', pk=pk, username=username)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        # user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        # 'user_form': user_form,
        'profile_form': profile_form
    })


class UserDeleteView(DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('/')
