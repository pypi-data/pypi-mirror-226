# Testing
Django PFX provides tools to ease API testing.

## APIClient
APIClient is a utility class to request the API in test classes.
It inherits from DjangoClient and add
locale and json response management.

If the response content_type is 'application/json',
the response contains a json_content
attributes with the deserialized json content.

### Locale

If your application is internationalized,
you can pass a default locale to the client
so that each request header contains
the HTTP_X_CUSTOM_LANGUAGE attribute with the locale.

Example :
```
client = APIClient(default_locale='en_GB')
```
Each request to a service can also override the locale.
Example :
```
client = APIClient()
response = client.get('/api/authors', locale='fr_CH')
```


### GET
Send a get request.

Example :
```
client = APIClient()
response = client.get('/api/authors')
```

### POST
Send a post request with content type 'application/json'.

Example :
```
client = APIClient()
response = client.post(
    '/api/authors', {
        'first_name': 'Arthur Charles',
        'last_name': 'Clarke'})
```

### PUT
Send a put request with content type 'application/json'.

Example :
```
client = APIClient()
response = self.client.put(
    f'/api/authors/{author_pk}',
    {'first_name': 'J. R. R.',
     'last_name': 'Tolkien'
     'slug': 'j-r-r-tolkien'})
```

### DELETE
Send a delete request with content type 'application/json'.

Example :
```
client = APIClient()
response = client.delete(
    f'/api/authors/{author_pk}')
```


### Login
If you use PFX authentication views you can use this login method.

Once you called login, you can call any other method
listed above, the authentication token will be sent with the requests.

Example :
```
client = APIClient()
client.login(
    username='jrr.tolkien',
    password='thepwd')

client.get('/api/authors')  # authenticated request.
```

## TestAssertMixin
TestAssertMixin provides useful method for your test class.

### assertRC
Test the response code of a response.
It takes two parameters, the response and the expected status code.

Example :
```
class ATestClass(TestAssertMixin, TransactionTestCase):

    def a_test(self):
        client = APIClient()
        response = client.post(
            '/api/authors', {
            'first_name': 'Arthur Charles',
            'last_name': 'Clarke'})
        self.assertRC(response, 200)
```

### assertJE
Test the value of a json property in the json_content of the response.
It takes 3 parameters, the response, the key and the expected value.
It allows you to specify the path to reach an element in the json structure.
For instance if you have a response like
```
{
    "author": {
        "pk": 2,
        "resource_name": "Philip Kindred Dick"
    },
    "name": "A Scanner Darkly",
    "pk": 6,
}
```
you can reach the author pk by providing "author.pk" as the key.

AssertJE also allows to specify the index in an array.
The syntax is "@index".

For instance if you want the pk of the author of the
third item in an array of books you can specify "items.@3.author.pk"

Example :
```
class ATestClass(TestAssertMixin, TransactionTestCase):

    def a_test(self):
        client = APIClient()
        response = client.get('/api/books')
        self.assertJE(response, 'items.@3.author.pk', 6)
```

### assertNJE
Assert NJE is the same as AssertJE, but it tests that the value is not equal.

## Print Response
You can use the print_response helper to print a response in the console.

Example :
```
client = APIClient()
response = client.get('/api/books')
print_response(response)
```

will produce

```
*********************http response*********************
Status :  200 OK
Headers :
  Content-Type: application/json
  Content-Length: 258
  X-Content-Type-Options: nosniff
  Referrer-Policy: same-origin
  Vary: Accept-Language
  Content-Language: en

Content :
{
    "author": {
        "pk": 2,
        "resource_name": "Philip Kindred Dick"
    },
    "created_at": "2022-01-15",
    "meta": {
        "message": "Book A Scanner Darkly updated."
    },
    "name": "A Scanner Darkly",
    "pk": 6,
    "pub_date": "1977-01-01",
    "resource_name": "A Scanner Darkly",
}
*******************************************************
```
