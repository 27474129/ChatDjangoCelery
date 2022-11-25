from django.http import HttpResponse
from .tasks import test_task


def root_page(request):
    test_task.delay()
    return HttpResponse("Success")
