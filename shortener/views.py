from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from .models import Link, Domain
from urllib.parse import urlparse
import hashlib
import datetime
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
import string

class HomePageView(TemplateView):
    """
    Display the home page (shortening url)
    """
    template_name = 'home.html'

class CountPageView(TemplateView):
    """
    Display the count page (get number of times a shortened URL is used)
    """
    template_name = 'count.html'

def shorten(request):
    """
    An endpoint that receives a URL and returns a new shortened URL
    """
    url = request.POST["url"]
    if url:
        parsed_url = urlparse(url)
        domain = parsed_url.hostname
        path = parsed_url.path
        
        # insert/update the domain in the requested url to the Domain table
        update_domain_model(domain) 
        # Use hash function to create a short unique code for the url
        shortenURL = hashlib.sha256(path.encode('utf-8')).hexdigest()[:8]
        try:
            check = Link.objects.get(shortenURL = shortenURL)
        except Link.DoesNotExist:
            entry = Link(shortenURL = shortenURL, url = url)
            entry.save()
        messages.success(request, 'It is done', extra_tags = shortenURL, fail_silently=True)
    return HttpResponseRedirect(reverse('home'))

def update_domain_model(domain):
    """
    Create a new domain entry (if not exist) or update the number
    of time a domain is requested

    There are 12 months in a year and each month's numerical value is 1, 2, 3, 4, etc
    so there are odd and even months
    Use odd and even in order to update the number of request, 
        if the current month is odd, save it to odd month, and so on
        if the system month has changed (different from current_month), 
        alternate to the other column (odd/even)
    """
    system_month = datetime.datetime.now().month #get current month on PC
    is_even = False if system_month%2 else True 
    try:
        d = Domain.objects.get(domain = domain)
    except Domain.DoesNotExist:
        if is_even:
            entry = Domain(domain = domain, current_month = system_month, even_month = system_month, odd_month = system_month - 1, even_month_num_visited = 1)
        else:
            entry = Domain(domain = domain, current_month = system_month, even_month = system_month - 1, odd_month = system_month, odd_month_num_visited = 1)
        entry.save()
    else:
        if system_month == d.current_month:
            if is_even: 
                d.even_month_num_visited += 1 
            else: 
                d.odd_month_num_visited += 1
        else:
            d.current_month = system_month
            if is_even: 
                d.even_month_num_visited = 1 
            else: 
                d.odd_month_num_visited = 1
        d.save()

def retrieve_url(request, shortenURL):
    """
    When a shortened URL is clicked, this function is called and it will
    redirect to the original link
    It also update the number of times a link is used
    """
    link_object = get_object_or_404(Link, shortenURL = shortenURL.strip(string.punctuation))
    link_object.numVisited += 1
    link_object.save()
    url = link_object.url
    if(url[:4] != 'http'):
        url = 'http://' + url
    return redirect(url)

def recent(request):
    """
    An endpoint to retrieve the last 100 shortened URLs
    """
    recent_100_links = Link.objects.order_by('-dateAdded')[:100]
    context = {'recent_100_links': recent_100_links}
    return render(request, 'recent.html', context)


def top(request):
    """
    An endpoint to retrieve the top 10 most popular shortened domains in the past month
    """
    system_month = datetime.datetime.now().month
    is_even = False if system_month%2 else True 
    if is_even:
        top_10_links = Domain.objects.filter(odd_month__exact=system_month - 1, current_month__exact=system_month).order_by('-odd_month_num_visited')[:10]
    else:
        top_10_links = Domain.objects.filter(even_month__exact=system_month - 1, current_month__exact=system_month).order_by('-even_month_num_visited')[:10]
    context = {'top_10_links': top_10_links}
    return render(request, 'top.html', context)


def count(request):
    """
    An endpoint to retrieve the number of times a shortened URL has been visited.
    """
    input_link = request.GET.get("short_url")
    if input_link:
        shortenURL = input_link[22:]
        link_object = get_object_or_404(Link, shortenURL = shortenURL)
        extra = f'{input_link} has been visited {link_object.numVisited} times'
        messages.success(request, 'Got the number', extra_tags = extra)
    return HttpResponseRedirect(reverse('count'))
