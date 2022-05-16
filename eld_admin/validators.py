import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_unit_year(value):
    current_year = datetime.datetime.now().year
    if value > current_year+1:
        raise ValidationError(
            _('Given "Year" value "%(value)s" is inappropriate'),
            params={'value': value},
        )


def validate_VIN(value):
    if not value.isdigit():
        raise ValidationError(_('"VIN" value must contain digits only'))
    if len(value) != 17:
        raise ValidationError(_('VIN" value length must be equal 17'))