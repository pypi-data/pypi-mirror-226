# Django PFX Views
REST services are provided as ViewMixin.
Each of these views must set the queryset used to query the model data either
by defining the queryset attribute or by overriding the get_queryset method.

Fields can be listed in the fields attribute, else all the fields are provided.

## ListRestViewMixin
Provide a list service for a model class.

By default, list fields are taken from fields attributes if defined.
They can also be listed in the list_fields attribute if you need to have
different fields in the list than in other views.
```
@rest_view("/books")
class BookRestView(ListRestViewMixinRestView):
    queryset = Book.objects
    list_fields = ['name', 'author', 'pub_date', 'created_at', 'type']
```
### Meta
### Pagination

### Filters
List view can have filters.

TODO explain filters.

## DetailRestViewMixin
Provide a get detail service for a model class.

```
@rest_view("/books")
class BookRestView(DetailRestViewMixin):
    queryset = Book.objects
    fields = ['name', 'author', 'pub_date', 'created_at', 'type']
```
### Meta

## CreateRestViewMixin
Provide a creation service for a model class.
Readonly fields can be provided in the read_only attribute.

TODO : explain "default_values"
```
@rest_view("/books")
class BookRestView(CreateRestViewMixin):
    queryset = Book.objects
    fields = ['name', 'author', 'pub_date', 'created_at', 'type']
    readonly_fields = ['created_at']
```

## UpdateRestViewMixin
Provide an update service for a model class.
Readonly fields can be provided in the read_only attribute.
```
@rest_view("/books")
class BookRestView(UpdateRestViewMixin):
    queryset = Book.objects
    fields = ['name', 'author', 'pub_date', 'created_at', 'type']
    readonly_fields = ['created_at']
```

## DeleteRestViewMixin
Provide a delete service for a model class.

```
@rest_view("/books")
class BookRestView(DeleteRestViewMixin):
    queryset = Book.objects
```

## SlugDetailRestViewMixin
Provide a get detail service for a model class with a slug.
Slug field is searched in the "slug" field of the model by default,
but it can be overridden with the "SLUG_FIELD" attribute.

```
@rest_view("/authors")
class AuthorRestView(SlugDetailRestViewMixin):
    queryset = Author.objects
    SLUG_FIELD = "slug"
    fields = ['name', 'slug', 'created_at', 'type']
```

## SecuredRestViewMixin
TODO Explain :
- default_public = True
- def perm(self):
- {func_name}_perm


## RestView
A base class that inherits :
        ListRestViewMixin,
        DetailRestViewMixin,
        CreateRestViewMixin,
        UpdateRestViewMixin,
        DeleteRestViewMixin,
        SecuredRestViewMixin,
        django.views.View
