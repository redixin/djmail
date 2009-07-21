from django.utils._threading_local import local

_local = local()

def get_current_user():
    print getattr(_local, 'user', None)
    return getattr(_local, 'user', None)

class UserMiddleware(object):
    def process_request(self, request):
        _local.user = getattr(request, 'user', None)

