from .custom_validators import password_validator, is_alpha_validator
from typing_extensions import Annotated
from pydantic import AfterValidator

# Кастомный тип пароля
PasswordStr = Annotated[str, AfterValidator(password_validator)]
# Кастомный тип на проверку строки, состоящей только из букв
AlphaStr = Annotated[str, AfterValidator(is_alpha_validator)]

