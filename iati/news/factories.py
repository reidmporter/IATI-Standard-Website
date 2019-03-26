import factory
from wagtail_factories import ImageFactory
from django.utils import timezone
from django.utils.text import slugify
from home.factories import BasePageFactory
from news.models import (
    NewsCategory,
    NewsIndexPage,
    NewsPage,
)


class NewsIndexPageFactory(BasePageFactory):
    """Factory generating data for NewsIndexPage."""

    class Meta:
        model = NewsIndexPage


class NewsPageFactory(BasePageFactory):
    """Factory generating data for NewsPage."""

    class Meta:
        model = NewsPage

    date = factory.fuzzy.FuzzyDate(
        start_date=timezone.now() - timezone.timedelta(weeks=520),
        end_date=timezone.now(),
    )
    feed_image = factory.SubFactory(ImageFactory)

    @factory.post_generation
    def news_categories(self, create, extracted, **kwargs):
        """Generate M2M for news categories."""
        if not create:
            return

        if extracted:
            for category in extracted:
                self.news_categories.add(category)


class NewsCategoryFactory(factory.django.DjangoModelFactory):
    """Factory generating data for NewsCategory snippet."""

    class Meta:
        model = NewsCategory

    name = factory.Faker(
        'sentence',
        nb_words=3,
    )
    name_fr = factory.Faker(
        'sentence',
        locale='fr_FR',
        nb_words=3,
    )
    name_es = factory.Faker(
        'sentence',
        locale='es_ES',
        nb_words=3,
    )
    name_es = factory.Faker(
        'sentence',
        locale='pt_PT',
        nb_words=3,
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
