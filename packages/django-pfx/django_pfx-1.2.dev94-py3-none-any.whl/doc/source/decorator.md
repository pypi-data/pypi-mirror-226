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
    @rest_api("/path/<int:id>/test/<slug:slug>", method="get")
    def class_method(self, id, slug):
```

## Registering urls
To be available, annotated view class must be registered
in your urls.py file as follows.
```
from django_request_mapping import UrlPattern

from . import views

urlpatterns = UrlPattern()
urlpatterns.register(views.BookRestView)
```
