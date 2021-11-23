from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django_messages.forms import ComposeForm
from django_messages.utils import get_username_field

from .filters import AdFilter
from .forms import AdForm, RentForm
from .models import Ad, Attachment

User = get_user_model()


def index(request):
    queryset = Ad.objects.all().order_by("-created_at")
    ad_filter = AdFilter(request.GET, queryset=queryset)

    page = request.GET.get("page")
    paginator = Paginator(queryset, 12)
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)
    return render(
        request,
        "ads/index.html",
        {"queryset": queryset, "filter": ad_filter, "ads": ads},
    )


def ad(request, slug):
    row = get_object_or_404(Ad, slug=slug)
    msg = Ad.objects.get(slug=slug)
    img = msg.images.all()
    user_ads = Ad.objects.filter(user=row.user)
    rented = Ad.objects.get(slug=slug).rent_set.all()
    form = RentForm(request.POST or None)
    if form.is_valid():
        rent_ad = form.save(commit=False)
        rent_ad.client = request.user
        rent_ad.ad = Ad.objects.get(slug=slug)
        rent_ad.save()
        success_url = reverse("ads:contact", kwargs={"slug": slug})
        return redirect(success_url)

    context = {
        "row": row,
        "img": img,
        "rented": rented,
        "form": form,
        "user_ads": user_ads,
    }
    return render(request, "ads/ad.html", context)


@login_required
def edit(request, pk):
    post = get_object_or_404(Ad, pk=pk)
    msg = Ad.objects.get(pk=pk)
    img = msg.images.all()[:3]
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("ads:index")
    else:
        form = AdForm(instance=post)

    context = {"form": form, "img": img, "post": post}
    return render(request, "ads/ad_edit.html", context)


@login_required
def contact(request, slug, recipient=None, success_url=None, recipient_filter=None):
    row = get_object_or_404(Ad, slug=slug)

    if request.method == "POST":
        # sender = request.user
        form = ComposeForm(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, "Message and email successfully sent.")
            if success_url is None:
                success_url = reverse("ads:ad", kwargs={"slug": slug})
            if "next" in request.GET:
                success_url = request.GET["next"]
            return HttpResponseRedirect(success_url)
    else:
        form = ComposeForm(
            initial={"recipient": row.user.username, "subject": row.title}
        )

        if recipient is not None:
            recipients = [
                u
                for u in User.objects.filter(
                    **{
                        "%s__in"
                        % get_username_field(): [
                            r.strip() for r in recipient.split("+")
                        ]
                    }
                )
            ]
            form.fields["recipient"].initial = recipients

    return render(request, "ads/contact.html", {"form": form})


class AdView(CreateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/form.html"
    success_url = reverse_lazy("ads:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AdView, self).form_valid(form)


class AdDeleteView(DeleteView):
    model = Ad

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("ads:index")


class AttachmentDeleteView(DeleteView):
    model = Attachment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.ad = self.object.ad
        self.object.delete()
        return redirect("/ads/edit/" + str(self.ad.id))


def filter(request):
    ad_filter = AdFilter(request.GET, queryset=Ad.objects.all().order_by("-created_at"))
    page = request.GET.get("page")
    paginator = Paginator(ad_filter.qs, 12)
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)

    context = {"filter": ad_filter, "ads": ads}
    return render(request, "ads/filter.html", context)


def search(request):
    queryset = Ad.objects.all().order_by("-created_at")
    query = request.GET.get("q")
    ad_filter = AdFilter(request.GET, queryset=Ad.objects.all())

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(category__icontains=query)
            | Q(brand__icontains=query)
            | Q(price__icontains=query)
            | Q(address__icontains=query)
            | Q(city__icontains=query)
            | Q(user__username__icontains=query)
        ).distinct()
    page = request.GET.get("page")
    paginator = Paginator(queryset, 12)
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "filter": ad_filter,
        "ads": ads,
        "q": query,
    }
    return render(request, "ads/search.html", context)
