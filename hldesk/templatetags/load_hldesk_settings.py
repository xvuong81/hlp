"""
django-hldesk - A Django powered ticket tracker for small enterprise.

templatetags/load_hldesk_settings.py - returns the settings as defined in
                                    django-hldesk/hldesk/settings.py
"""
from __future__ import print_function
from django.template import Library
from hldesk import settings as hldesk_settings_config


def load_hldesk_settings(request):
    try:
        return hldesk_settings_config
    except Exception as e:
        import sys
        print("'load_hldesk_settings' template tag (django-hldesk) crashed with following error:",
              file=sys.stderr)
        print(e, file=sys.stderr)
        return ''


register = Library()
register.filter('load_hldesk_settings', load_hldesk_settings)
