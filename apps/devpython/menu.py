from django.urls import reverse

menu = {
    'devlanguagemodule': {
        'child': [
            {'name': 'python', 'title': 'Python', 'href':  reverse('devpython:index')},
        ]
    },
}
