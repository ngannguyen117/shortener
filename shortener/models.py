from django.db import models
from datetime import datetime

class Link(models.Model):
    url = models.CharField(max_length=2083)
    shortenURL = models.CharField(max_length=8,primary_key=True)
    numVisited = models.IntegerField(default = 0)
    dateAdded = models.DateTimeField(default=datetime.now, editable=False)

    def __str__(self):
        return self.shortenURL

class Domain(models.Model):
    domain = models.CharField(max_length=253,primary_key=True)
    current_month = models.IntegerField()
    odd_month = models.IntegerField()
    even_month = models.IntegerField()
    odd_month_num_visited = models.IntegerField(default = 0)
    even_month_num_visited = models.IntegerField(default = 0)

    def __str__(self):
        return self.domain