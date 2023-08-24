# Getting Started with PFX

## Install django pfx

Using pip
```
pip install django-pfx
```

## Configuration

Add pfxcore to the installed app

```
INSTALLED_APPS = [
    'pfx.pfxcore',
]
```

## Create your services

### Model class
Create a simple model class.
```
from django.db import models


class Book(models.Model):
    BOOK_TYPES = [
        ('science_fiction', 'Science Fiction'),
        ('heroic_fantasy', 'Heroic Fantasy'),
        ('detective', 'Detective')]

    title = models.CharField("Title", max_length=30)
    author = models.CharField("Author", max_length=150)
    type = models.CharField("Type", max_length=20, choices=BOOK_TYPES)
    pub_date = models.DateField("Pub Date")
    created_at = models.DateField("Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.name}"

```

### Views
Create a new view
```
from pfx.pfxcore.decorator import rest_view
from pfx.pfxcore.views import DetailRestViewMixin

from book.models import Book


@rest_view("/books")
class BookRestView(DetailRestViewMixin):
    default_public = True
    queryset = Book.objects
    fields = ['title', 'author', 'type', 'pub_date', 'created_at']
```

### URLs
Register the url in urls.py.
```
from django.urls import path, include
from django_request_mapping import UrlPattern

from book import views

apipatterns = register_views(views.BookRestView)

urlpatterns = [
    path('api/', include(apipatterns)),
]
```

### Request the app in test
Create a test class to test this new API.
