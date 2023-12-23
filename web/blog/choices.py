from datetime import timedelta, datetime

from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from enum import Enum


class ArticleStatus(IntegerChoices):
    INACTIVE = (0, _('Inactive'))
    ACTIVE = (1, _('Active'))


class DatetimeEnum(Enum):
    CURRENT_YEAR = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    SINCE_LAST_DAY = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)