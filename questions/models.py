from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qus = models.CharField(max_length=256, verbose_name="question")
    details = RichTextUploadingField()
    slug = models.SlugField(unique=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name="question_likes")
    views = models.PositiveIntegerField(default=0)
    has_accepted_answer = models.BooleanField(default=False)
    tags = TaggableManager()

    def __str__(self):
        return self.qus

    def get_absolute_url(self):
        return reverse("questions:question_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-created"]

    def _get_unique_slug(self):
        slug = slugify(self.qus)
        unique_slug = slug
        num = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Question, self).save()

    def get_answer_count(self):
        return Question.objects.filter(answer__question=self).count()

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_accepted=True)

    def get_like_url(self):
        return reverse("questions:like-toggle", kwargs={"slug": self.slug})


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans = RichTextUploadingField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.question.qus

    class Meta:
        ordering = ["-created"]
