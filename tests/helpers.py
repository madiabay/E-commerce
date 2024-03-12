import json

from rest_framework_simplejwt.tokens import AccessToken


def access_token(user):
    return f'Bearer {AccessToken.for_user(user)}'


def load_json_data(path: str):
    with open(f'tests/data/{path}.json') as file:
        return json.load(file)
