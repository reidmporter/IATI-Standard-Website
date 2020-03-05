"""A module of unit tests for contact."""
import pytest
from django.http import HttpRequest
from django import forms

from contact.zendeskhelper import generate_ticket

LEGITIMATE_USER = {}
LEGITIMATE_USER['request'] = HttpRequest()
LEGITIMATE_USER['request'].path = "/en/a-test-path"
LEGITIMATE_USER['form'] = forms.Form()
LEGITIMATE_USER['form'].cleaned_data = {
    'phone': '',
    'email': 'test@user.com',
    'textarea': 'A very serious matter.',
    'name': 'A legitimate user',
    'skip_captcha_check': True
}
LEGITIMATE_USER.expected_output = {
    'request': {
        'requester': {
            'name': 'A legitimate user',
            'email': 'test@user.com'
        },
        'comment': {
            'body': 'A request was sent from /en/a-test-path.\nA very serious matter.'
        },
        'subject': 'Automated request from A legitimate user'
    }
}


SPAM_BOT = {}
SPAM_BOT['request'] = HttpRequest()
SPAM_BOT['request'].path = "/en/a-test-path"
SPAM_BOT['form'] = forms.Form()
SPAM_BOT['form'].cleaned_data = {
    'phone': '555-555-5555',
    'email': 'test@user.com',
    'textarea': 'A very serious matter.',
    'name': 'A legitimate user',
    'skip_captcha_check': False
}
SPAM_BOT.expected_output = False


@pytest.mark.parametrize("user", [LEGITIMATE_USER, SPAM_BOT])
def test_generate_ticket(user):
    """Test a ticket from a valid user and a spam bot."""
    ticket = generate_ticket(user['request'], user['form'])
    assert ticket == user.expected_output
