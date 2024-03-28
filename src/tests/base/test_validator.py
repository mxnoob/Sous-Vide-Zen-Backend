import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


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
