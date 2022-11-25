from django.urls import path
from .views import root_page


urlpatterns = [
    path("", root_page, name="root")
]
