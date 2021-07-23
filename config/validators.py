from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not any(letter.isdigit() for letter in password):
            raise ValidationError(
                _("パスワードは数字を最低1文字含む必要があります。"),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "パスワードは数字を最低1文字含む必要があります。"
        )
