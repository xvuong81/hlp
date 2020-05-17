# -*- coding: utf-8 -*-
from django.urls import reverse
from django.test import TestCase

from hldesk.models import KBCategory
from hldesk.tests.helpers import get_user, reload_urlconf


class TestKBDisabled(TestCase):
    def setUp(self):
        from hldesk import settings

        self.HELPDESK_KB_ENABLED = settings.HELPDESK_KB_ENABLED
        if self.HELPDESK_KB_ENABLED:
            settings.HELPDESK_KB_ENABLED = False
            reload_urlconf()

    def tearDown(self):
        from hldesk import settings

        if self.HELPDESK_KB_ENABLED:
            settings.HELPDESK_KB_ENABLED = True
            reload_urlconf()

    def test_navigation(self):
        """Test proper rendering of navigation.html by accessing the dashboard"""
        from django.urls import NoReverseMatch

        self.client.login(username=get_user(is_staff=True).get_username(), password='password')
        self.assertRaises(NoReverseMatch, reverse, 'hldesk:kb_index')
        try:
            response = self.client.get(reverse('hldesk:dashboard'))
        except NoReverseMatch as e:
            if 'hldesk:kb_index' in e.message:
                self.fail("Please verify any unchecked references to hldesk_kb_index (start with navigation.html)")
            else:
                raise
        else:
            self.assertEqual(response.status_code, 200)

    def test_public_homepage_with_kb_category(self):
        KBCategory.objects.create(title="KB Cat 1",
                                  slug="kbcat1",
                                  description="Some category of KB info")
        response = self.client.get(reverse('hldesk:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hldesk/public_homepage.html')


class TestDecorator(TestCase):

    def test_staff_member_restrictions(self):
        user = get_user(username='hldesk.user',
                        password='password')

        self.client.login(username=user.get_username(),
                          password='password')
        response = self.client.get(reverse('hldesk:list'))
        self.assertEqual(response.status_code, 403)

    def test_staff_member_access(self):
        user = get_user(username='hldesk.user',
                        password='password',
                        is_staff=True)

        self.client.login(username=user.get_username(),
                          password='password')
        response = self.client.get(reverse('hldesk:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hldesk/ticket_list.html')

    def test_superuser_member_restrictions(self):
        user = get_user(username='hldesk.superuser',
                        password='password',
                        is_staff=True)

        self.client.login(username=user.get_username(),
                          password='password')
        response = self.client.get(reverse('hldesk:email_ignore'))
        self.assertEqual(response.status_code, 403)

    def test_superuser_member_access(self):
        user = get_user(username='hldesk.superuser',
                        password='password',
                        is_staff=True,
                        is_superuser=True)

        self.client.login(username=user.get_username(),
                          password='password')
        response = self.client.get(reverse('hldesk:email_ignore'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hldesk/email_ignore_list.html')
