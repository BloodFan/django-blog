from django.utils.translation import gettext_lazy as _

error_messages = {
    'not_verified': _('Email not verified'),
    'not_active': _('Your account is not active. Please contact Your administrator'),
    'wrong_credentials': _('Entered email or password is incorrect'),
    'already_registered': _('User is already registered with this e-mail address'),
    'password_not_match': _('The two password fields did not match'),
    'incorrect_birthday': _('date of birth is incorrect'),
}
