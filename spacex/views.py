from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import Launch
from ast import literal_eval


def get_launch_status(launch: dict) -> str:
    success = launch.get("success", False)
    upcoming = launch.get("upcoming", False)
    if success:
        return "S"
    elif upcoming:
        return "U"
    return "F"


def create_launch_dbtable(api_url=""):
    with open("spaceX.json") as f:
        launches = literal_eval(f.read())

    for launch in launches:
        name = launch.get("name")
        image_url = launch.get("links", {}).get("patch", {}).get("large")
        details = launch.get("details")
        article_link = launch.get("links", {}).get("article")
        reddit_link = launch.get("links", {}).get("reddit", {}).get("launch")
        wikipedia_link = launch.get("links", {}).get("wikipedia")
        date = launch.get("date_utc")
        status = get_launch_status(launch)
        Launch.objects.create(
            name=name,
            image=image_url,
            details=details,
            article_link=article_link,
            reddit_link=reddit_link,
            wikipedia_link=wikipedia_link,
            status=status,
            date=date.split("T")[0],
        )


# ../update/list/?filter=filter-val&orderby=order-val
#
# and get the filter and orderby in the get_queryset like:
#
# class MyView(ListView):
#     model = Update
#     template_name = "updates/update.html"
#     paginate_by = 10
#
#     def get_queryset(self):
#         filter_val = self.request.GET.get('filter', 'give-default-value')
#         order = self.request.GET.get('orderby', 'give-default-value')
#         new_context = Update.objects.filter(
#             state=filter_val,
#         ).order_by(order)
#         return new_context
#
#     def get_context_data(self, **kwargs):
#         context = super(MyView, self).get_context_data(**kwargs)
#         context['filter'] = self.request.GET.get('filter', 'give-default-value')
#         context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
#         return context


class HomeView(ListView):
    model = Launch
    template_name = "index.html"
    paginate_by = 10

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "launch_list.html"
        return self.template_name

    def get_queryset(self):
        if status := self.request.GET.get("status"):
            if status != "all":
                context = Launch.objects.filter(status=status)
                return context
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["status"] = self.request.GET.get("status", "")
        return context
