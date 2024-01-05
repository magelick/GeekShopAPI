from .custom_validators import password_validator, is_alpha_validator, title_validator, age_validator
from typing_extensions import Annotated
from pydantic import AfterValidator

# Кастомный тип пароля
PasswordStr = Annotated[str, AfterValidator(password_validator)]
# Кастомный тип на проверку строки, состоящей только из букв
AlphaStr = Annotated[str, AfterValidator(is_alpha_validator)]
# Кастомный тип на проверку наличия символов, отличающихся от пробела, цифр и букв
TitleStr = Annotated[str, AfterValidator(title_validator)]
# Кастомный тип на проверку введённого возраста
AgeInt = Annotated[int, AfterValidator(age_validator)]