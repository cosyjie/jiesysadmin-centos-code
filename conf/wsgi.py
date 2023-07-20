import os

from django.core.wsgi import get_wsgi_application
# import socketio
# import eventlet
# import eventlet.wsgi
# from apps.system.view_xterm import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

application = get_wsgi_application()

# django_app = get_wsgi_application()
# application = socketio.WSGIApp(sio, django_app, static_files={'/static': 'static/'})
# eventlet.wsgi.server(eventlet.listen(('', 8000)), application, debug=True)

