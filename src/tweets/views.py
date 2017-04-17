
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms.utils import ErrorList
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import TweetModelForm

# custom mixins
from .mixins import FormUserNeededMixin, UserOwnerMixin
# import models
from .models import Tweet


# Create your views here.

# CRUD
# create, retrieve, update, delete

"""
Function Based Views
"""

# def tweet_create_view(request):
#     form = TweetModelForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()

#     context = {
#         'form': form
#     }
#     return render(request, 'tweet/create_view.html', context)

# def tweet_detail_view(request, pk=None):
#     # obj = Tweet.objects.get(pk=pk) # GET from database
#     obj = get_object_or_404(Tweet, pk=pk)
#     context = {
#         'object': obj,
#     }
#     return render(request, "tweets/detail_view.html", context)


# def tweet_list_view(request):
#     queryset = Tweet.objects.all()
#     # print(queryset)

#     # for obj in queryset:
#     #     print(obj.content)

#     context = {
#         'object_list': queryset
#     }
#     return render(request, "tweets/list_view.html", context)


"""
Class Based Views
"""

class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(tweet.get_absolute_url())

class TweetCreateView(FormUserNeededMixin, CreateView):
    # queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    # success_url = '/tweet/create' # where user is redirected if successfully completed request
    # success_url = reverse_lazy('tweet:detail')
    login_url = '/admin/' # will redirect user if not logged in b/c of LoginRequiredMixin


    # fields = [
    #     'user',
    #     'content'
    # ]


    #### moved to mixins ###
    # def form_valid(self, form):
    #     if self.request.user.is_authenticated():
    #     # need `instance` of the obj
    #         form.instance.user = self.request.user
    #         return super(TweetCreateView, self).form_valid(form)
    #     else:
    #         form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User must be logged in to continue.'])
    #         return self.form_invalid(form) # form_invalid is built-in

# update
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    # success_url = '/tweet'
    template_name = 'tweets/update_view.html'
    # default login_url if not stated

# delete
class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/delete_confirm.html'
    success_url = reverse_lazy('tweet:list') # refers to the `name` in urls.py


# retrieving
class TweetDetailView(DetailView):
    template_name = 'tweets/detail_view.html'
    queryset = Tweet.objects.all()

    def get_object(self):
        # print(self.kwargs)
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Tweet, pk=pk)
        # return Tweet.objects.get(id=pk)
        return obj

class TweetListView(LoginRequiredMixin, ListView):
    template_name = 'tweets/list_view.html'
    # queryset = Tweet.objects.all()
    def get_queryset(self, *args, **kwargs):
        im_following = self.request.user.profile.get_following()

        # combining querysets
        qs1 = Tweet.objects.filter(user__in=im_following)
        qs2 = Tweet.objects.filter(user=self.request.user)
        qs = (qs1 | qs2).distinct().order_by("-timestamp")
        # print(self.request.GET)
        query = self.request.GET.get('q', None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)

        # can add custom key:value pair
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweet:create')
        # print(context)

        return context
