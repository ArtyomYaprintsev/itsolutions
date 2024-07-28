from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
)


class Token(BaseModel):
    """Authorization token scheme."""
    access_token: str
    type: str = 'bearer'


class UserPassword(BaseModel):
    """User password scheme."""
    password: str = Field(max_length=50, min_length=8)


class LoginUser(UserPassword):
    """User login credentials scheme."""
    email: EmailStr = Field(
        max_length=50,
        examples=['example@xyz.com'],
    )


class SignupUser(LoginUser):
    """User signup credentials scheme.

    Provides additional `confirm_password` field. It is used to check if
    passwords match.
    """
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(
        cls,
        confirm_password_value: str,
        info: ValidationInfo,
        **kwargs,
    ):
        """Validate that password match.

        Raises:
            `ValueError`: if passwords do not match.
        """
        if (
            'password' in info.data
            and confirm_password_value != info.data['password']
        ):
            raise ValueError('Passwords do not match')
        return confirm_password_value
