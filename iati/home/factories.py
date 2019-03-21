import factory
import factory.fuzzy
from wagtail_factories import PageFactory
from django.utils.text import slugify
from wagtail.core.models import Page
from home.models import StandardPage


class BasePageFactory(PageFactory):
    """Factory generating data for all Page models."""

    class Meta:
        model = Page
        abstract = True

    title = factory.Faker(
        'sentence',
        nb_words=4,
    )
    title_en = factory.LazyAttribute(lambda obj: obj.title)
    title_fr = factory.Faker(
        'sentence',
        locale='fr_FR',
        nb_words=4,
    )
    title_es = factory.Faker(
        'sentence',
        locale='es_ES',
        nb_words=4,
    )
    title_pt = factory.Faker(
        'sentence',
        locale='pt_PT',
        nb_words=4,
    )
    slug_en = factory.LazyAttribute(lambda obj: slugify(obj.title_en))
    slug_fr = factory.LazyAttribute(lambda obj: slugify(obj.title_fr))
    slug_es = factory.LazyAttribute(lambda obj: slugify(obj.title_es))
    slug_pt = factory.LazyAttribute(lambda obj: slugify(obj.title_pt))
    url_path_fr = factory.LazyAttribute(lambda obj: '{}/'.format(obj.slug_fr))
    url_path_es = factory.LazyAttribute(lambda obj: '{}/'.format(obj.slug_es))
    url_path_pt = factory.LazyAttribute(lambda obj: '{}/'.format(obj.slug_pt))
    heading = factory.Faker(
        'sentence',
    )
    heading_fr = factory.Faker(
        'sentence',
        locale='fr_FR',
        nb_words=6,
    )
    heading_es = factory.Faker(
        'sentence',
        locale='es_ES',
        nb_words=6,
    )
    heading_pt = factory.Faker(
        'sentence',
        locale='pt_PT',
        nb_words=6,
    )
    excerpt = factory.Faker(
        'paragraph',
    )
    excerpt_fr = factory.Faker(
        'paragraph',
        locale='fr_FR',
    )
    excerpt_es = factory.Faker(
        'paragraph',
        locale='es_ES',
    )
    excerpt_pt = factory.Faker(
        'paragraph',
        locale='pt_PT',
    )


class StandardPageFactory(BasePageFactory):
    """Factory generating data for StandardPage models."""

    class Meta:
        model = StandardPage

    fixed_page_type = factory.fuzzy.FuzzyChoice(
        choices=('privacy', 'terms', 'trans', None)
    )
