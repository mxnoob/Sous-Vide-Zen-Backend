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
