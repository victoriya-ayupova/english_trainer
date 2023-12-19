from werkzeug.security import check_password_hash
from wtforms import Form, StringField, EmailField, PasswordField

from auth.models import User


class LoginForm(Form):
    email = EmailField('Email')
    password = PasswordField('Password')

    # def validate_email(self, field: EmailField) -> None:
    #     user = User.get_or_none(User.email == field.data)
    #     if user is None:
    #         raise validators.ValidationError('Пользователя с таким email не существует')
    #
    # def validate_password(self, field: PasswordField) -> None:
    #     user = User.get_or_none(User.email == self.email.data)
    #     if not check_password_hash(user.password, field.data):
    #         raise validators.ValidationError('Неверный пароль')

    def validate(self, extra_validators=None) -> bool:
        if not super().validate(extra_validators):
            return False

        user = User.get_or_none(User.email == self.email.data)
        if user is None:
            self.email.errors.append('Такого пользователя не существует')
            return False
        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Неверный пароль')
            return False
        return True


class RegisterForm(Form):
    name = StringField('Name')
    email = EmailField('Email')
    password = PasswordField('Password')

    def validate(self, extra_validators=None) -> bool:
        if not super().validate(extra_validators):
            return False

        user = User.get_or_none(User.email == self.email.data)
        if user is not None:
            self.email.errors.append(f'У пользователя с email {self.email.data} уже есть аккаунт')
            return False
        return True


class PasswordRecoveryForm(Form):
    email = EmailField('Email')
    password = PasswordField('Новый пароль')

    def validate(self, extra_validators=None) -> bool:
        if not super().validate(extra_validators):
            return False

        user = User.get_or_none(User.email == self.email.data)
        if user is None:
            self.email.errors.append('Такого пользователя не существует')
            return False
        return True

