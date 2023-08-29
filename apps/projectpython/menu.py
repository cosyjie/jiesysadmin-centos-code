from django.urls import reverse

menu = {
    'projectmodule': {
        'child': [
            {'name': 'pythonprojects', 'title': 'Python项目', 'href':  reverse('devpython:index')},
        ]
    },
}
