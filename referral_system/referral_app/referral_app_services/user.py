import datetime
from typing import Tuple

import jwt

from exceptions import ErrorType, AppError
from referral_app.models import UserProfile

import random


class UserAccount:

    def create_update_user(self, phone_number: str) -> Tuple[str, str]:
        """
        User logs in to the system by phone number.
        :param phone_number: string containing the user's phone number
        :return: authentication code and JWT
        """
        user = UserProfile.objects.filter(phone_number=phone_number)
        authentication_code = self.generating_authentication_code()
        access_token = self.create_jwt()
        if user:
            user.update(authentication_code=authentication_code, access_token=access_token)
            # self.send_notification([phone_number], f'{authorization_code}')
        else:
            invite_code = self.generating_invite_code()
            UserProfile.objects.create(
                phone_number=phone_number,
                authentication_code=authentication_code,
                invite_code=invite_code,
                access_token=access_token
            )
            # self.send_notification([phone_number], f'{authorization_code}')
        return authentication_code, access_token

    @staticmethod
    def check_authentication_code(authentication_code, access_token) -> None:
        """
        User authentication by phone number code and cookies.
        :param access_token: the string contains a JWT
        :param authentication_code: the string contains a four-digit code
        :raises AppError: if invalid code entered
        """
        user = UserProfile.objects.filter(access_token=access_token).first().authentication_code
        if user == authentication_code:
            pass
        else:
            raise AppError(
                {
                    'error_type': ErrorType.TOKEN_ERROR,
                    'description': 'invalid authentication code entered'
                }
            )

    @staticmethod
    def activate_invite_code(access_token, invite_code) -> None:
        """
        User activates the invite code.
        :param invite_code: the string contains the invitation code
        :param access_token: the string contains a JWT
        :raises AppError: if invalid invite code entered
        """
        user_invite = UserProfile.objects.filter(invite_code=invite_code).first()
        if user_invite:
            UserProfile.objects.filter(access_token=access_token).update(used_code=invite_code)
        else:
            raise AppError(
                {
                    'error_type': ErrorType.INVITE_ERROR,
                    'description': 'invalid invite code entered'
                }
            )

    @staticmethod
    def get_user_info(access_token) -> dict:
        """
        Get user information.
        :param access_token: the string contains a JWT
        :raises AppError: if invalid invite code entered
        """
        user = UserProfile.objects.filter(access_token=access_token).first()
        if user:
            data_user = {
                'phone_number': user.phone_number,
                'invite_code': user.invite_code,
                'used_code': user.used_code
            }
            dependent_user = UserProfile.objects.filter(used_code=user.invite_code)
            data_user['dependent_user'] = [user.phone_number for user in dependent_user]
            return data_user
        else:
            raise AppError(
                {
                    'error_type': ErrorType.TOKEN_ERROR,
                    'description': 'invalid jwt'
                }
            )

    @staticmethod
    def create_jwt():
        """
        Creating JWT.
        :return:
        """
        payload = {"sub": "admin",
                   "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=2)
                   }
        return jwt.encode(payload, '123', algorithm="HS256")

    @staticmethod
    def generating_authentication_code() -> str:
        """
        Generating an authentication token.
        :return:
        """
        numbers = random.sample(range(10), 4)
        return ''.join(map(str, numbers))

    @staticmethod
    def generating_invite_code() -> str:
        """
        Generating an invitation token.
        :return:
        """
        return ''.join([random.choice(list('123456789!@#$%*+')) for _ in range(6)])

    # @staticmethod
    # def send_notification(phone_number: list[str], txt: str) -> None: