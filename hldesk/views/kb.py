"""
django-hldesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

views/kb.py - Public-facing knowledgebase views. The knowledgebase is a
              simple categorised question/answer system to show common
              resolutions to common problems.
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from hldesk import settings as hldesk_settings
from hldesk.models import KBCategory, KBItem


def index(request):
    category_list = KBCategory.objects.all()
    # TODO: It'd be great to have a list of most popular items here.
    return render(request, 'hldesk/kb_index.html', {
        'kb_categories': category_list,
        'hldesk_settings': hldesk_settings,
    })


def category(request, slug):
    category = get_object_or_404(KBCategory, slug__iexact=slug)
    items = category.kbitem_set.all()
    return render(request, 'hldesk/kb_category.html', {
        'category': category,
        'items': items,
        'hldesk_settings': hldesk_settings,
    })


def item(request, item):
    item = get_object_or_404(KBItem, pk=item)
    return render(request, 'hldesk/kb_item.html', {
        'item': item,
        'hldesk_settings': hldesk_settings,
    })


def vote(request, item):
    item = get_object_or_404(KBItem, pk=item)
    vote = request.GET.get('vote', None)
    if vote in ('up', 'down'):
        item.votes += 1
        if vote == 'up':
            item.recommendations += 1
        item.save()

    return HttpResponseRedirect(item.get_absolute_url())
