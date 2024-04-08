import pytest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from src.base.validators import (
    CustomPasswordValidator,
    NoLowerCaseValidator,
    NoUpperCaseValidator,
    NoNumbersValidator,
)


@pytest.mark.parametrize(
    "password",
    [
        "short",
        "NOLOWERCASE123!",
        "nouppercase123!",
        "NoSpecial123",
        "NoNumbers!!",
        "ValidPassword123!",
    ],
)
def test_password_validators(password):
    """
    Test all configured password validators
    """
    # Если пароль "ValidPassword123!", то он должен быть действительным
    if password == "ValidPassword123!":
        # Пароль должен быть принят всеми валидаторами без ошибок
        try:
            validate_password(password)
        except ValidationError as e:
            pytest.fail(
                f"ValidPassword123! should be a valid password, but failed with {e}"
            )
    else:
        # Для всех остальных паролей ожидаем ValidationError
        with pytest.raises(ValidationError):
            validate_password(password)


@pytest.mark.parametrize(
    "validator_class, expected_help_text",
    [
        (
            CustomPasswordValidator,
            "Пароль должен состоять не менее чем из 8 символов: минимум с одной прописной (a-z) и одной заглавной буквой (A-Z), минимум с одной цифрой (0-9) и одним специальным символом (!@#$%^&*).",
        ),
        (
            NoLowerCaseValidator,
            "Пароль должен содержать хотя бы одну строчную букву (a-z, а-я).",
        ),
        (
            NoUpperCaseValidator,
            "Пароль должен содержать хотя бы одну заглавную букву (A-Z, А-Я).",
        ),
        (NoNumbersValidator, "Пароль должен содержать хотя бы одну цифру (0-9)."),
    ],
)
def test_validator_help_texts(validator_class, expected_help_text):
    validator = validator_class()
    help_text = validator.get_help_text()
    assert (
        help_text == expected_help_text
    ), f"{validator_class.__name__} help text did not match expected"
