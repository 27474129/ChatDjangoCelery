import logging
from chat.celery_ import app
from celery.utils.log import get_task_logger
from core.models import ChatMessages, PersonalMessages, Users, Mailing


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@app.task
def send_message(data):
    logger.info(data)
    message = ChatMessages.objects.create(message=data["message"])
    message.who_sent.add(data["who_sent"])


@app.task
def register_mailing_message(user_id: int, mailing_id: int):
    user = Users.objects.get(pk=user_id)
    mailing_data = Mailing.objects.get(pk=mailing_id)

    PersonalMessages.objects.create(message=mailing_data.message, recipient=user, image=mailing_data.image)
