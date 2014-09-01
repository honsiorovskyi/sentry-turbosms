"""
sentry_turbosms.plugin
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Denis Gonsiorovsky.
:license: BSD, see LICENSE for more details.
"""

import logging
import mysql.connector as MySQLdb
import sentry_turbosms

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from sentry.constants import LOG_LEVELS
from sentry.plugins.bases.notify import NotificationPlugin
from sentry.utils.safe import safe_execute


class TurboSMSOptionsForm(forms.Form):
    numbers = forms.CharField(
        label=_('Phone numbers'),
        widget=forms.Textarea(attrs={
            'class': 'span6', 'placeholder': '+380xxyyyyyyy'}),
        help_text=_('Enter phone numbers to send new events to (one per line).')
    )
    login = forms.CharField(
        label=_('Login'),
        help_text=_('TurboSMS login'),
        validators=[RegexValidator(r'\w+')]
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
        help_text=_('TurboSMS password')
    )
    alphaname = forms.CharField(
        label=_('Alphaname'),
        help_text=_('TurboSMS alphaname'),
        validators=[RegexValidator(r'\w+')]
    )
    level = forms.ChoiceField(
        label=_('Level'),
        choices=LOG_LEVELS.items()
    )


class TurboSMSPlugin(NotificationPlugin):
    author = 'Denis Gonsiorovsky'
    author_url = 'https://github.com/gonsiorovsky'
    version = sentry_turbosms.VERSION
    description = "Integrates TurboSMS."
    resource_links = [
        ('Bug Tracker', 'https://github.com/gonsiorovsky/sentry-turbosms/issues'),
        ('Source', 'https://github.com/gonsiorovsky/sentry-turbosms'),
    ]

    slug = 'turbosms'
    title = _('TurboSMS')
    conf_title = title
    conf_key = 'turbosms'
    project_conf_form = TurboSMSOptionsForm
    logger = logging.getLogger('sentry.plugins.turbosms')
    user_agent = 'sentry-turbosms/%s' % version

    def is_configured(self, project, **kwargs):
        return bool(
            self.get_option('numbers', project) and
            self.get_option('login', project) and
            self.get_option('password', project)
        )

    def get_turbosms_numbers(self, project):
        numbers = self.get_option('numbers', project)
        if not numbers:
            return ()
        return filter(bool, numbers.strip().splitlines())

    def send_turbosms(self, number, login, alphaname, message, cur):
        cur.execute(
            "INSERT INTO `" + login + "`(number, sign, message) VALUES (%s, %s, %s)",
            (number, alphaname, message)
        )

    def notify_users(self, group, event, fail_silently=False):
        if group.level < int(self.get_option('level', group.project)):
            return

        message = ('%s: %d / %s' % (group.project.slug, group.id, event.message))[:160]

        login = self.get_option('login', group.project)
        password = self.get_option('password', group.project)
        alphaname = self.get_option('alphaname', group.project)

        db = safe_execute(
            MySQLdb.connect,
            host='94.249.146.189',
            user=login,
            passwd=password,
            db='users'
        )

        cur = safe_execute(db.cursor)

        for number in self.get_turbosms_numbers(group.project):
            safe_execute(self.send_turbosms, number, login, alphaname, message, cur)

        safe_execute(db.commit)
        safe_execute(db.close)
