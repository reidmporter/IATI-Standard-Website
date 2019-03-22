import pytest
import random
from datetime import datetime
from django.conf import settings
from django.utils.translation import activate
from events.factories import EventIndexPageFactory, EventPageFactory, EventTypeFactory
from home.factories import StandardPageFactory
from home.models import HomePage, StandardPage
from home.templatetags.iati_tags import (
    event_type_verbose,
    check_active,
    default_page_url,
    haspassed,
    standard_page_url,
    translation_links,
    twopartdate,
)


@pytest.fixture()
def events():
    """Fixture to create batched EventPage tree."""
    home_page = HomePage.objects.first()
    event_page_index = EventIndexPageFactory(
        parent=home_page,
        title='Events',
    )
    event_types = EventTypeFactory.create_batch(3)
    event_pages = EventPageFactory.create_batch(
        10,
        parent=event_page_index,
        event_type=[random.choice(event_types)]
    )

    return event_page_index


@pytest.fixture()
def standard_pages():
    """Fixture to create batched StandardPages."""
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
        """Return HomePage instance."""
        return HomePage.objects.first()

    def test_default_home_page_url(self, client):
        """Test for return of relative URL for HomePage."""
        homepage_context = client.get(self.get_homepage.url, follow=False)
        default_url = default_page_url(homepage_context)
        assert default_url == ''

    def test_default_event_page_url(self, client, events):
        """Test for return of relative URL for EventPage."""
        events_response = client.get(events.url, follow=True)
        default_event_url = default_page_url(
            context=events_response.context,
            default_page_name='events',
        )
        assert default_event_url == events_response.request.get('PATH_INFO')
        assert default_event_url != ''

    def test_check_active(self, client, events):
        """Test for return of active class string for Events."""
        events_response = client.get(events.url, follow=True)
        active_class = check_active(
            context=events_response.context,
            urlname='events',
            nav_type='utility',
        )
        assert active_class == 'navigation-utility__item--active'

    def test_check_active_for_child(self, client, events):
        """Test for return of active class string for Events children."""
        event_child = events.get_children().first()
        events_response = client.get(event_child.url, follow=True)
        active_class = check_active(
            context=events_response.context,
            urlname='events',
        )
        assert active_class == 'navigation-utility__item--active'

    def test_standard_page_url(self, client, standard_pages):
        """
        Test the Standard Page URL based on page type.

        Assumes that one page instance exists for each page type
        """
        standard_pages = standard_pages.filter(fixed_page_type='terms')
        standard_page = standard_pages.first()
        standard_page_response = client.get(standard_page.url, follow=True)

        # workaround to add request as attribute to mimic RequestContext
        setattr(standard_page_response.context, 'request', standard_page_response.request)
        standard_page_url_response = standard_page_url(
            context=standard_page_response.context,
            page_type=standard_page.fixed_page_type
        )
        assert standard_page_url_response == standard_page.url

    @pytest.mark.skip(
        reason='Template tag only handles the first Standard Page of a '
               'specific fixed page type.'
    )
    def test_standard_page_url_for_null_page_type(self, client, standard_pages):
        """Test the Standard Page URL based on null page type."""
        standard_pages = standard_pages.filter(fixed_page_type__isnull=True)
        standard_page = standard_pages.first()
        standard_page_response = client.get(standard_page.url, follow=True)

        # workaround to add request as attribute to mimic RequestContext
        setattr(
            standard_page_response.context,
            'request',
            standard_page_response.request
        )
        with pytest.raises(TypeError) as e:
            standard_page_url(
                context=standard_page_response.context,
            )
        assert 'missing 1 required positional argument' in str(e)

    def test_translation_links(self, client, standard_pages):
        """Test translation links for active languages."""
        standard_page = standard_pages.first()
        response = client.get(standard_page.url, follow=True)
        translations = translation_links(response.context, standard_page)
        languages = translations['languages']
        fr_language = next(item for item in languages if item['code'] == 'fr')
        translation_response = client.get(fr_language['url'])
        assert translation_response.status_code == 200
        assert len(languages) == len(settings.ACTIVE_LANGUAGES)

    def test_time_haspassed(self):
        """Test past date returns True for haspassed."""
        past_date = datetime.strptime('Jan 1 2000', '%b %d %Y')
        assert haspassed(past_date) is True

    def test_two_part_date_different_dates(self):
        """Test two part date with different dates."""
        from django.utils.translation import activate
        activate('en')
        date_start = datetime(2019, 3, 2, 9, 0)
        date_end = datetime(2019, 5, 9, 9, 0)
        two_part_date = twopartdate(date_start, date_end)
        assert two_part_date['part1'].startswith('March 2, 2019')
        assert two_part_date['part2'].startswith('May 9, 2019')

    def test_two_part_date_same_dates(self):
        """Test two part date with same date, different times."""
        activate('en')
        date_start = datetime(2019, 3, 2, 9, 0)
        date_end = datetime(2019, 3, 2, 15, 0)
        two_part_date = twopartdate(date_start, date_end)
        assert two_part_date.get('part2_is_time')
        assert two_part_date.get('part2') == '9 a.m.–3 p.m.'

    @pytest.mark.skip(
        reason='No validation currently exists for start date and end date.'
    )
    def test_two_part_date_invalid_dates(self):
        """Test two part date with different dates."""
        activate('en')
        date_start = datetime(2019, 5, 9, 9, 0)
        date_end = datetime(2019, 3, 2, 9, 0)
        two_part_date = twopartdate(date_start, date_end)
        assert two_part_date['part1'] > two_part_date['part2']

    def test_event_type_verbose_slug(self, client, events):
        """Test that event name is returned for slug."""
        event = events.get_children().specific().first()
        an_event_type = event.event_type.first()
        verbose_event_type = event_type_verbose(an_event_type.slug)
        assert an_event_type.name == verbose_event_type

    @pytest.mark.skip(
        reason='Localization hasn not been added for event types'
    )
    def test_event_type_verbose_slug_localized(self, client, events):
        """Test localized event type."""
        event = events.get_children().specific().last()
        an_event_type = event.event_type.first()
        activate('fr')
        verbose_event_type = event_type_verbose(an_event_type.slug_fr)
        assert an_event_type.name_fr == verbose_event_type
