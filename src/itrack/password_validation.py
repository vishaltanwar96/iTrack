import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class BaseValidator(object):
    """."""

    pattern = None
    validator_msg_type = None
    validator_code = None

    def __init__(self, min_pattern_required=1):
        """."""

        if not all(
            (
                self.pattern,
                self.validator_msg_type,
                self.validator_code,
                isinstance(self.pattern, str),
            )
        ):
            raise ValidationError(
                message="BaseValidator can't be used directly, it must be overridden",
                code="base_validator_used_directly",
            )

        self.min_pattern_required = min_pattern_required
        self.err_msg = "Password must contain atleast %d %s" % (
            self.min_pattern_required,
            self.validator_msg_type,
        )

    def validate(self, password, user=None):
        """."""

        if not len(re.findall(self.pattern, password)) >= self.min_pattern_required:
            raise ValidationError(
                message=_(self.err_msg),
                code=self.validator_code,
            )

    def get_help_text(self):
        """."""

        return _(self.err_msg)


class UpperCaseValidator(BaseValidator):
    """Validates Uppercase Character in passwords."""

    pattern = r"[A-Z]"
    validator_msg_type = "uppercase character"
    validator_code = "password_no_uppercase"


class LowerCaseValidator(BaseValidator):
    """Validates Lowercase Character in passwords."""

    pattern = r"[a-z]"
    validator_msg_type = "lowercase character"
    validator_code = "password_no_lowercase"


class DigitValidator(BaseValidator):
    """Validates Uppercase Character in passwords."""

    pattern = r"\d"
    validator_msg_type = "digit"
    validator_code = "password_no_digit"


class SpecialCharacterValidator(BaseValidator):
    """Validates Uppercase Character in passwords."""

    pattern = r'[!@#$%^&*(),.?":{}|<>]'
    validator_msg_type = "special character"
    validator_code = "password_no_spec_char"
