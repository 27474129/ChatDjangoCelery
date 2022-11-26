import logging
from django.http import HttpResponse
from .tasks import send_message, register_mailing_message
from django.views import View
from django.views.generic import FormView, TemplateView
from .models import ChatMessages, PersonalMessages, Users
from .forms import ChatMessageForm, AuthForm, PersonalMessagesForm, MailingForm
from django.urls import reverse_lazy, reverse
from .services import AuthService
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta


logger = logging.getLogger("debug")


class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return HttpResponse(e)


class IndexView(BaseView, FormView):
    template_name = "core/index.html"
    form_class = ChatMessageForm
    success_url = reverse_lazy("root")

    def post(self, request, *args, **kwargs):
        send_message.delay(request.POST)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = ChatMessages.objects.all()
        if len(messages) != 0:
            context["messages"] = messages
        return context


class AuthView(BaseView, FormView):
    template_name = "core/auth.html"
    form_class = AuthForm
    success_url = reverse_lazy("root")

    def post(self, request, *args, **kwargs):
        AuthService.execute_service(request)
        return super().post(request, *args, **kwargs)


class LogoutPage(LogoutView):
    next_page = reverse_lazy("root")


class PersonalMessagesView(BaseView, TemplateView):
    template_name = "core/personal_messages.html"

    def get(self, request, *args, **kwargs):
        if not request.session.keys:
            return HttpResponseRedirect(reverse("root"))

        kwargs["user_id"] = request.session.get("user_id")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personal_messages = PersonalMessages.objects.filter(recipient=kwargs["user_id"])
        if len(personal_messages) != 0:
            context["personal_messages"] = personal_messages
            context["is_empty"] = False
        else:
            context["is_empty"] = True
        return context


class MailingView(BaseView, TemplateView):
    template_name = "core/mailing.html"

    def get(self, request, *args, **kwargs):
        if "is_super_user" not in request.session:
            return HttpResponse("Страница недоступна", status=404)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing_id = form.save().pk
            starttime = datetime.now() + timedelta(minutes=1)

            users = Users.objects.all()
            for user in users:
                if not user.is_super_user:
                    register_mailing_message.apply_async((user.pk, mailing_id), eta=starttime)

        return HttpResponseRedirect(reverse("mailing"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MailingForm()
        return context
