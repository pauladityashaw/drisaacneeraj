from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Post, Subscriber
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .forms import SearchForm, EmailPostForm

import random

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.db import IntegrityError

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    form = EmailPostForm()
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/list.html',
                   {'page': page,
                    'posts': posts,
                    'form':form})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/detail.html', {'post':post})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    return render(request,
                  'blog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

def new_email(request):
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            try:
                new_sub = form.cleaned_data
                sub = Subscriber(email=new_sub['email'], conf_num = random_digits())
                sub.save()
                # message = Mail(
                # from_email=settings.FROM_EMAIL,
                # to_emails=sub.email,
                # subject='Blog Confirmation',
                # html_content='Thank you for signing up for my Blog ! \
                #     Please complete the process by \
                #     <a href="{}/confirm/?email={}&conf_num={}"> clicking here to \
                #     confirm your registration</a>.'.format(request.build_absolute_uri('/confirm/'),
                #                                         sub.email,
                #                                         sub.conf_num))
                # sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                # response = sg.send(message)
                # print(response)
                message = "Confirmation Message sent to your email :)"
            except IntegrityError:
                message = "You are already subscribed :)"
            return render(request, 'blog/validate.html', {'message':message})