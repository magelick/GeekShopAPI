from .user import UserLoginForm, UserRegisterForm, UserDetail
from .device import DeviceDetail, DeviceAddFrom
from .character import CharacterDetail, CharacterAddForm
from .comics import ComicsDetail, ComicsAddForm
from .sweet import SweetDetail, SweetAddForm
from .toy import ToyDetail, ToyAddForm
from .universe import UniverseDetail, UniverseAddForm
from .аuthor import AuthorDetail, AuthorAddForm
from .settings import Settings

__all__ = [
    "UserDetail",
    "UserLoginForm",
    "UserRegisterForm",

    "DeviceDetail",
    "DeviceAddFrom",

    "CharacterDetail",
    "CharacterAddForm",

    "ComicsDetail",
    "ComicsAddForm",

    "SweetDetail",
    "SweetAddForm",

    "ToyDetail",
    "ToyAddForm",

    "UniverseDetail",
    "UniverseAddForm",

    "AuthorDetail",
    "AuthorAddForm",

    "Settings"
]