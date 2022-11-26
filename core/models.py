from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=40)
    # TextField т.к. необходимо хранить хэш пароля а не сам пароль, в будущем имеется ввиду
    password = models.TextField()
    is_super_user = models.BooleanField(default=False)


class PersonalMessages(models.Model):
    message = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey("Users", on_delete=models.CASCADE)
    image = models.TextField()


# решил не хранить сообщения в брокере redis или в любой NoSQL DB т.к. будет непросто получать данные и выводить их,
# и сохранять порядок
class ChatMessages(models.Model):
    message = models.TextField()
    who_sent = models.ManyToManyField(Users)


class Mailing(models.Model):
    message = models.TextField()
    image = models.ImageField(null=True, upload_to="photos/%Y/%m/%d/")
