from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserGenderStatus(IntegerChoices):
    NOT_KHOWN = (0, _('Not_known'))  # что к чему относится?
    MALE = (1, _('Male'))
    FEMALE = (2, _('Female'))
    NOT_APPLICABLE = (9, _('Not_applicable'))
