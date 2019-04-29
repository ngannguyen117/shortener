from django.urls import path
from django.contrib import admin
from .views import HomePageView, CountPageView, shorten, recent, top, count, retrieve_url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('top/', top, name='top'),
    path('shorten/', shorten, name='shorten'),
    path('recent/', recent, name='recent'),
    path('count/', CountPageView.as_view(), name='count'),
    path('count/result', count, name='count_result'),
    path('<shortenURL>/', retrieve_url, name='retrieve'),
]
