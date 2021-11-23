from django.db.models import Count
from django.shortcuts import render
from django.views.generic.base import TemplateView

from ads.models import Ad


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context["categories"] = Ad.objects.values("category").annotate(
            Count("category")
        )
        return context


def offline(request):
    return render(request, "offline.html")
