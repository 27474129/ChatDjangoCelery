import logging
from .models import Users


logger = logging.getLogger("debug")


# уже был готовый код со старого проекта, убрал хеширование, решил использовать
class AuthService:
    @staticmethod
    def __check_data(entered_username: str, entered_password: str) -> int or None:
        user = Users.objects.filter(username=entered_username)
        if len(user) == 0:
            return None

        if user[0] is None:
            return None

        return user[0] if entered_password == user[0].password else None

    @staticmethod
    def __authenticate(request, user_id: int, username: str, is_super_user: bool = False) -> None:
        request.session.set_expiry(1296000)
        request.session["user_id"] = user_id
        request.session["username"] = username
        if is_super_user:
            request.session["is_super_user"] = True

    @staticmethod
    def execute_service(request) -> bool:
        entered_username = request.POST["username"]
        entered_password = request.POST["password"]

        verification_result = AuthService.__check_data(entered_username, entered_password)
        if type(verification_result) is Users:
            AuthService.__authenticate(request, verification_result.pk, entered_username, verification_result.is_super_user)
            logger.debug("Authenticated")
            return True
        else:
            logger.debug("Incorrect username or password")
            return False
