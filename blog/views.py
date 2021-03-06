from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Post
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .forms import SearchForm

import random

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
                    'posts': posts})

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