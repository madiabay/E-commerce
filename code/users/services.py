import random
import uuid
from time import sleep
from typing import Protocol, OrderedDict

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import tokens
from mobizon_client import MobizonClient

from . import repos
import logging
logger = logging.getLogger(__name__)


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> None: ...

    def create_token(self, data: OrderedDict) -> dict: ...

    def verify_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        return self._verify_phone_number(data=data)

    def verify_user(self, data: OrderedDict) -> None:
        user_data = cache.get(data['session_id'])

        if not user_data:
            raise ValidationError
        if data['code'] != user_data['code']:
            raise ValidationError

        user = self.user_repos.create_user(data={
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
        self._send_letter_to_email(email=user.email)

    def create_token(self, data: OrderedDict) -> dict:
        user = self.user_repos.get_user(data=data) # проверка на наличие user
        return self._verify_phone_number(data=data)

    def verify_token(self, data: OrderedDict) -> dict:
        session = cache.get(data['session_id'])
        if not session:
            raise ValidationError

        if session['code'] != data['code']:
            raise ValidationError

        user = self.user_repos.get_user(data={'phone_number': session['phone_number']})
        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access),
            'refresh': str(refresh),
        }

    def _verify_phone_number(self, data: OrderedDict) -> dict:
        code = self._generate_code()
        session_id = self._generate_session_id()
        cache.set(session_id, {**data, 'code': code}, timeout=300)
        self._send_sms_to_phone_number(phone_number=data['phone_number'], code=code)
        # self._mobizon(phone_number=data['phone_number'][1:], code=code)
        return {'session_id': session_id}

    @staticmethod
    def _generate_code(length: int = 4) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _send_letter_to_email(email: str) -> None:
        send_mail(
            "WELCOME!!!",
            "IT'S MADI'S SITE",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def _send_sms_to_phone_number(phone_number: str, code: str) -> None:
        logger.info(f'send sms code {code} to {phone_number}')

    @staticmethod
    def _mobizon(phone_number: str, code: str):
        url = 'https://api.mobizon.kz'
        api_key = 'kza3095687d4a6080881fe37a80ba33cff4e5581c9d82db6e90b5095e84f1ef2628174'
        client = MobizonClient(url=url, api_key=api_key)
        result = client.send_message(recipient=phone_number, text=f'send sms code {code} from MADI',
                                     sender_signature=None)
        sleep(3)
        result = client.get_message_status([result.message_id])
        print()
        print(result[0].status)
        print()
        # assert result[0].status == 'DELIVRD'
        client.close()

