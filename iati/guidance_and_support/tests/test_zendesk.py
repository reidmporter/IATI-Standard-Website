"""A module of unit tests for guidance and support."""
import requests
import pytest
from django.http import HttpRequest
from django.conf import settings

from guidance_and_support.zendeskhelper import generate_ticket


@pytest.fixture
def legitimate_user():
    """Create legitimate user request for testing."""
    legitimate_user = HttpRequest()
    legitimate_user.path = "/en/a-test-path"
    legitimate_user.POST = {
        'phone': '',
        'email': 'test@user.com',
        'textarea': 'A very serious matter.',
        'name': 'A legitimate user'
    }
    legitimate_user.expected_output = {
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
    return legitimate_user


@pytest.fixture
def spam_user():
    """Create spam user request for testing."""
    spam_bot = HttpRequest()
    spam_bot.path = "/en/a-test-path"
    spam_bot.POST = {
        'phone': '555-555-5555',
        'email': 'test@user.com',
        'textarea': 'A very serious matter.',
        'name': 'A legitimate user'
    }
    spam_bot.expected_output = False
    return spam_bot


@pytest.mark.django_db
class TestZendesk():
    """Unit test for Zendesk API."""

    def test_api_client(self, client):
        """Perform GET on endpoint URL to verify a response."""
        api_key = settings.TEST_ZENDESK_API_KEY
        user = '{}/token'.format(settings.TEST_ZENDESK_USER_EMAIL)
        auth = (user, api_key)
        endpoint = settings.ZENDESK_REQUEST_URL

        if not any(x for x in auth):
            pytest.skip(
                'API key env var does not exist, test cannot proceed'
            )

        response = requests.get(endpoint, auth=auth)
        assert response.status_code == 200

    def test_generate_ticket_legitimate(self, legitimate_user):
        """Test generate ticket function for legtimate user."""
        ticket = generate_ticket(legitimate_user)
        assert ticket == legitimate_user.expected_output

    def test_generate_ticket_spam(self, spam_user):
        """Test generate ticket for spam user."""
        ticket = generate_ticket(spam_user)
        assert ticket == spam_user.expected_output
