import logging
from django import template


logger = logging.getLogger("debug")


register = template.Library()


def get_username_by_id(who_sent):
    for elem in who_sent.all():
        return elem.username


register.filter("get_username_by_id", get_username_by_id)
