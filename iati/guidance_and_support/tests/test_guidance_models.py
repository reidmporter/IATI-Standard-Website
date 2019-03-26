import pytest
from guidance_and_support.factories import (
    GuidanceAndSupportPageFactory,
    GuidanceGroupPageFactory,
    GuidancePageFactory
)
from guidance_and_support.models import GuidancePage
from home.models import HomePage


@pytest.fixture
def guidance():
    """Fixture for guidance models."""
    home_page = HomePage.objects.first()
    guidance_and_support_index = GuidanceAndSupportPageFactory.create(
        parent=home_page
    )
    guidance_group_live = GuidanceGroupPageFactory(
        parent=guidance_and_support_index
    )
    guidance_group_draft = GuidanceGroupPageFactory(
        parent=guidance_and_support_index,
        live=False,
    )
    GuidancePageFactory.create_batch(
        20,
        parent=guidance_group_live
    )
    GuidancePageFactory.create_batch(
        20,
        parent=guidance_group_draft,
        live=False,
    )
    return guidance_and_support_index


@pytest.mark.django_db
class TestGuidancePage():
    """Tests EventPage."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_guidance_tree(self, client, guidance):
        """Test that event with random date is created."""
        guidance_group_pages = guidance.get_children().specific()
        guidance_pages = GuidancePage.objects.descendant_of(guidance)
        guidance_group_page_draft = guidance_group_pages.filter(live=False).first()
        assert guidance_group_page_draft.guidance_groups == []
        assert guidance.guidance_groups.count() == 1
        assert guidance_pages.count() == 40
