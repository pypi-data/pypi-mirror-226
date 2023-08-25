# View decorator and URL
## @rest_view
Used to provide the base path of a view class
```
@rest_view("/base-path")
class ViewClass():
```

## @rest_api
Used to annotate the rest services method.
Parameters are the path and the HTTP method.
```
@rest_api("/path", method="get")
def class_method(self):
```

A short example
```
@rest_view("/books")
class BookRestView():

    @rest_api("/list", method="get")
    def get_list(self):
        return JsonResponse(
            dict(books=['The Man in the High Castle', 'A Scanner Darkly']))
```

### path parameters
Path can contain parameters that are passed to the method.
```
@rest_api("/path/<int:pk>/test/<slug:slug>", method="get")
def class_method(self, pk, slug):
```

## Registering urls
To be available, annotated view class must be registered
in your urls.py file as follows.
```
from pfx.pfxcore import register_views

from . import views

urlpatterns = register_views(
    views.AuthorRestView,
    views.BookRestView)
```
You can include multiple views under one path, or add a path
wih a specific class method for each HTTP methods:
```
from pfx.pfxcore import register_views

from . import views

urlpatterns = [
    path('api/', include(register_views(
        views.AuthorRestView,
        views.BookRestView))),
    path('other/thing', views.OtherRestView.as_view(
        pfx_methods=dict(get='get_other'))),
]
```
