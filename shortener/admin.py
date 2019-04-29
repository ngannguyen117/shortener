from django.contrib import admin

from .models import Link, Domain

admin.site.register(Link)
admin.site.register(Domain)