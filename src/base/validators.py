from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall("[!@#$%^&*]", password):
            raise ValidationError(
                _(
                    "Пароль должен содержать хотя бы один специальный символ (!@#$%^&*)."
                ),
                code="password_no_special",
            )

    def get_help_text(self):
        return _(
            "Пароль должен состоять не менее чем из 8 символов:"
            " минимум с одной прописной (a-z) и одной заглавной буквой (A-Z),"
            " минимум с одной цифрой (0-9) и одним специальным символом (!@#$%^&*)."
        )


class NoLowerCaseValidator:
    def validate(self, password, user=None):
        if not re.findall("[a-z, а-я]", password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну строчную букву (a-z, а-я)."),
                code="password_no_lower",
            )

    def get_help_text(self):
        return _("Пароль должен содержать хотя бы одну строчную букву (a-z, а-я).")


class NoUpperCaseValidator:
    def validate(self, password, user=None):
        if not re.findall("[A-Z, А-Я]", password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву (A-Z, А-Я)."),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Пароль должен содержать хотя бы одну заглавную букву (A-Z, А-Я).")


class NoNumbersValidator:
    def validate(self, password, user=None):
        if not re.findall("[0-9]", password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну цифру (0-9)."),
                code="password_no_number",
            )

    def get_help_text(self):
        return _("Пароль должен содержать хотя бы одну цифру (0-9).")
