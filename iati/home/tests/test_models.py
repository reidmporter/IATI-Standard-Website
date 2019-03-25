import pytest
from about.factories import CaseStudyPageFactory, CaseStudyIndexPageFactory
from home.models import HomePage


@pytest.fixture()
def case_studies():
    """Fixture to create batched EventPage tree."""
    home_page = HomePage.objects.first()
    case_study_index = CaseStudyIndexPageFactory(
        title='Case Studies',
        parent=home_page
    )
    CaseStudyPageFactory.create_batch(
        size=20,
        parent=case_study_index
    )

    return case_study_index


@pytest.mark.django_db
class TestHomePage():
    """Tests for Home Page."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_home_page_lists_all_case_studies(self, client, case_studies):
        """Test that case studies are passed to HomePage context."""
        home_page_context = client.get(self.home_page.url, follow=True).context
        home_page_case_studies = home_page_context.get('case_studies', None)
        case_study_pages = case_studies.get_children()

        assert len(case_study_pages) == len(home_page_case_studies)

    def test_home_page_lists_live_case_studies(self, client, case_studies):
        """Test that only live case studies are passed to context."""
        CaseStudyPageFactory.create_batch(
            size=10,
            parent=case_studies,
            live=False,
        )

        home_page_context = client.get(self.home_page.url, follow=True).context
        home_page_case_studies = home_page_context.get('case_studies', None)

        assert len(home_page_case_studies) == 20
