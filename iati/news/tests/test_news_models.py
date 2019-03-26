import pytest
from news.factories import (
    NewsIndexPageFactory,
    NewsPageFactory,
    NewsCategoryFactory,
)
from news.models import NewsPage
from home.models import HomePage


@pytest.fixture()
def news():
    """Fixture to create batched NewsIndexPage tree."""
    home_page = HomePage.objects.first()
    news_page_index = NewsIndexPageFactory(
        parent=home_page,
        title='News',
    )
    news_categories = NewsCategoryFactory.create_batch(3)
    for category in news_categories:
        NewsPageFactory.create_batch(
            20,
            parent=news_page_index,
            news_categories=[category]
        )
    return news_page_index


@pytest.mark.django_db
class TestNewsPage():
    """Tests EventPage."""

    @property
    def home_page(self):
        """Return HomePage created in migrations."""
        return HomePage.objects.first()

    def test_news_categories_type(self, client, news):
        """Test that event with random date is created."""
        news_category = news.news_categories.first()
        news_category_slug = news_category.slug
        pages_with_category = NewsPage.objects.filter(
            news_categories__slug=news_category_slug
        ).all()
        response = client.get(
            news.url,
            {'type': news_category_slug},
            follow=True
        )
        filtered_posts_count = response.context['news_posts'].paginator.count
        assert filtered_posts_count == pages_with_category.count()
        assert news.news_categories.count() == 3
