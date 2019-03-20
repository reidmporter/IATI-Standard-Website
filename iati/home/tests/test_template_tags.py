import pytest
from events.factories import EventIndexPageFactory, EventPageFactory
from home.factories import StandardPageFactory
from home.models import HomePage, StandardPage
from home.templatetags.iati_tags import (
    check_active,
    default_page_url,
    standard_page_url,
)


@pytest.fixture()
def events():
    home_page = HomePage.objects.first()
    event_page_index = EventIndexPageFactory(
        parent=home_page,
        title='Events',
    )
    EventPageFactory.create_batch(10, parent=event_page_index)
    return event_page_index


@pytest.fixture()
def standard_pages():
    home_page = HomePage.objects.first()
    standard_pages = StandardPageFactory.create_batch(
        20,
        parent=home_page,
    )
    page_ids = [x.id for x in standard_pages]
    return StandardPage.objects.filter(id__in=page_ids).all()


@pytest.mark.django_db
class TestTemplateTags():
    """Tests for template tags."""

    @property
    def get_homepage(self):
        return HomePage.objects.first()

    def test_default_home_page_url(self, client):
        homepage_context = client.get(self.get_homepage.url, follow=False)
        default_url = default_page_url(homepage_context)
        assert default_url == ''

    def test_default_event_page_url(self, client, events):
        events_response = client.get(events.url, follow=True)
        default_event_url = default_page_url(
            context=events_response.context,
            default_page_name='events',
        )
        assert default_event_url == events_response.request.get('PATH_INFO')
        assert default_event_url != ''

    def test_check_active(self, client, events):
        events_response = client.get(events.url, follow=True)
        active_class = check_active(
            context=events_response.context,
            urlname='events',
            nav_type='utility',
        )
        assert active_class == 'navigation-utility__item--active'

    def test_check_active_for_child(self, client, events):
        event_child = events.get_children().first()
        events_response = client.get(event_child.url, follow=True)
        active_class = check_active(
            context=events_response.context,
            urlname='events',
        )
        assert active_class == 'navigation-utility__item--active'

    def test_standard_page_url(self, client, standard_pages):
        """
        Testing the Standard Page URL based on page type assuming that
        one page type exists for each page type.
        """

        standard_pages = [x for x in standard_pages if x.fixed_page_type == 'terms']
        standard_page = standard_pages[0]
        standard_page_response = client.get(standard_page.url, follow=True)

        # workaround to add request as attribute to mimic RequestContext
        setattr(standard_page_response.context, 'request', standard_page_response.request)
        standard_page_url_response = standard_page_url(
            context=standard_page_response.context,
            page_type=standard_page.fixed_page_type
        )
        assert standard_page_url_response == standard_page.url

    # @pytest.mark.skip(reason="no way of currently testing this")
    # def test_standard_page_url_for_blank_page_type(self, client, standard_pages):
    #     standard_pages = standard_pages.filter(fixed_page_type__isnull=True)
    #     standard_page = standard_pages.first()
    #     standard_page_response = client.get(standard_page.url, follow=True)

    #     # workaround to add request as attribute to mimic RequestContext
    #     setattr(standard_page_response.context, 'request', standard_page_response.request)
    #     standard_page_url_response = standard_page_url(
    #         context=standard_page_response.context,
    #         page_type=standard_page.fixed_page_type
    #     )
    #     assert standard_page_url_response == ''
    # @register.simple_tag(takes_context=True)
    # def standard_page_url(context, page_type):
    #     """Return the relative url for other fixed pages based on the StandardPage."""
    #     standard_page = StandardPage.objects.live().filter(fixed_page_type=page_type).first()
    #     if standard_page is None or not hasattr(context, 'request'):
    #         return ''
    #     return standard_page.get_url(context['request'])
