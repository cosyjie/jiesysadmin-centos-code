from django.urls import reverse

menu = {
    'devlanguage': {
        'child': [
            {'name': 'python', 'title': 'Python', 'href':  reverse('devpython:index')},
        ]
    },
}
