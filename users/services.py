import random
import uuid
from time import sleep
from typing import Protocol, OrderedDict

from django.core.cache import cache
from rest_framework_simplejwt import tokens
from mobizon_client import MobizonClient

from . import repos


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> None: ...

    def create_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        numbers = [str(i) for i in range(10)]
        code = ''.join(random.choices(numbers, k=4))
        session_id = str(uuid.uuid4())
        session = {'code': code, **data}
        cache.set(session_id, session, timeout=300)
        self._send_sms_to_phone_number(phone_number=data['phone_number'], code=code)
        self._mobizon(phone_number=data['phone_number'][1:], code=code)

        return {'session_id': session_id}

    def verify_user(self, data: OrderedDict) -> None:
        user_data = cache.get(data['session_id'])

        if not user_data:
            return
        if data['code'] != user_data['code']:
            raise ValueError

        user = self.user_repos.create_user(data={
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
        self._send_letter_to_email(email=user.email)

    @staticmethod
    def _send_letter_to_email(email: str) -> None:
        print(f'send letter to {email}')

    @staticmethod
    def _send_sms_to_phone_number(phone_number: str, code: str) -> None:
        print(f'send sms code {code} to {phone_number}')

    @staticmethod
    def _mobizon(phone_number: str, code: str):
        url = 'https://api.mobizon.kz'
        api_key = 'kza3095687d4a6080881fe37a80ba33cff4e5581c9d82db6e90b5095e84f1ef2628174'
        client = MobizonClient(url=url, api_key=api_key)
        result = client.send_message(recipient=phone_number, text=f'send sms code {code} from MADI', sender_signature=None)
        sleep(3)
        result = client.get_message_status([result.message_id])
        print()
        print(result[0].status)
        print()
        # assert result[0].status == 'DELIVRD'
        client.close()

    def create_token(self, data: OrderedDict) -> dict:
        user = self.user_repos.get_user(data=data)

        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access),
            'refresh': str(refresh),
        }
