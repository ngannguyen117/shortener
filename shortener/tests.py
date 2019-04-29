from django.test import TestCase, RequestFactory
from .models import Link, Domain
from django.urls import reverse
from .views import shorten, count
from django.http import HttpRequest
from django.contrib.messages import get_messages  
import datetime

class LinkModelTest(TestCase):
    def setUp(self):
        shortenURL = "SamPleUR"
        url = "https://stackoverflow.com/questions/6303548/is-it-possible-to-make-multi-level-template-inheritance-in-django-templates"
        Link.objects.create(shortenURL = shortenURL, url = url)

    def test_Link_content(self):
        url = Link.objects.get(shortenURL = "SamPleUR")
        self.assertEqual(url.shortenURL, "SamPleUR")
        self.assertEqual(url.url, "https://stackoverflow.com/questions/6303548/is-it-possible-to-make-multi-level-template-inheritance-in-django-templates")

class DomainModelTest(TestCase):
    def setUp(self):
        Domain.objects.create(domain = "stackoverflow.com", current_month = 4, even_month = 4, odd_month = 3, even_month_num_visited = 1)

    def test_Link_content(self):
        domain = Domain.objects.get(domain = "stackoverflow.com")
        self.assertEqual(domain.domain, "stackoverflow.com")
        self.assertEqual(domain.even_month_num_visited, 1)

class ShortenedTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.shorten_url = "5864585d"   #the actual hash value return through the hashing 
                                        #function hashlib.sha256 from the test link
        self.link = "https://stackoverflow.com/questions/6303548/is-it-possible-to-make-multi-level-template-inheritance-in-django-templates"
        self.domain = "stackoverflow.com"

    def test_home_page_exists_at_proper_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_url_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_home_page_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')

    def test_shorten(self):
        post_request = self.factory.post('/', {'url': self.link})
        response = shorten(post_request)

        self.assertEqual(Link.objects.all()[0].shortenURL, self.shorten_url)
        self.assertEqual(Link.objects.all()[0].url, self.link)
        self.assertEqual(response.status_code, 302)

    def test_update_domain_model(self):
        """ Test if the domain table is added/updated when a new link is requested"""
        post_request = self.factory.post('/', {'url': self.link})
        shorten(post_request)

        domain_object = Domain.objects.get(domain = self.domain)
        
        self.assertEqual(domain_object.domain, self.domain)
        self.assertEqual(domain_object.current_month, 4)
        self.assertEqual(domain_object.even_month_num_visited, 1) # 1 request => 1 time

        # second request, same domain
        link = "https://stackoverflow.com/questions/47062227/writing-a-django-unit-test-for-a-function-with-a-httpresponse"
        post_request = self.factory.post('/', {'url': link})
        shorten(post_request)
        domain_object = Domain.objects.get(domain = self.domain)
        self.assertEqual(domain_object.even_month_num_visited, 2) # 2 requests => 2 times

        # third request, same domain
        post_request = self.factory.post('/', {'url': self.link})
        shorten(post_request)
        domain_object = Domain.objects.get(domain = self.domain)
        self.assertEqual(domain_object.even_month_num_visited, 3) # 2 requests => 2 times

    def test_count(self):
        """ Test if the count view takes a request of a shortened url, and redirect to the page /count/"""
        request = self.factory.post('/count/', {'short_url': f'http://127.0.0.1:8000/{self.shorten_url}'})
        response = count(request) #the actual url that process the form is /count/result which calls count
        self.assertEqual(response.status_code, 302) #redirect to /count/ which is CountPageView view class


class Test(TestCase):
    def test_top(self):
        response = self.client.get('/top/')
        assert response.status_code == 200

    def test_recent(self):
        response = self.client.get('/recent/')
        assert response.status_code == 200

