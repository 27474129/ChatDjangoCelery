from django.urls import path
from chat import settings
from django.conf.urls.static import static
from .views import (
    IndexView, AuthView, LogoutPage,
    PersonalMessagesView, MailingView
)


urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("logout/", LogoutPage.as_view(), name="logout"),
    path("personalmessages/", PersonalMessagesView.as_view(), name="personalmessages"),
    path("mailing/", MailingView.as_view(), name="mailing"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
