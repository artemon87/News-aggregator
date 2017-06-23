# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.shortcuts import redirect
import feedparser
import datetime

def articles_list(request):
	articles = Article.objects.all()

	rows = [articles[i:i+1] for i in range(0, len(articles), 1)]


	return render(request, 'news/articles_list.html', {'rows' : rows})

def feeds_list(request):
	feeds = Feed.objects.all()
	return render(request, 'news/feeds_list.html', {'feeds' : feeds})
# Create your views here.
def new_feed(request):
	if request.method == 'POST':
		form = FeedForm(request.POST)
		if form.is_valid():
			feed = form.save(commit=False)

			existing = Feed.objects.filter(url = feed.url)
			if len(existing) == 0:
				feedData = feedparser.parse(feed.url) #feed.url is my url
				feed.title = feedData.feed.title
				feed.save()

				for entry in feedData.entries:
					article = Article()
					article.title = entry.title
					article.url = entry.link
					d = datetime.datetime(*(entry.published_parsed[0:6]))
					dateString = d.strftime('%Y-%m-%d %H:%M:%S')
					article.publication_date = dateString 
					article.description = entry.description
					article.feed = feed
					article.save()

			return redirect('feeds_list')
	else:
		form = FeedForm()
	return render(request, 'news/new_feed.html', {'form' : form}) 