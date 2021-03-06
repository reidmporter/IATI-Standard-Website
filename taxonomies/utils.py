from django.db.models import Q, Count
from django.utils.text import capfirst, slugify


def get_active_taxonomy_list(taxonomy, filters, **kwargs):
    """Return active taxonomy items, with an optional item count."""
    filter_obj = Q()
    order_by = kwargs.get('order_by', 'title')

    if kwargs.get('bespoke'):
        filter_obj = filters
    else:
        for item in filters:
            filter_obj &= Q(**{item: filters[item]})

    query = (taxonomy.objects
             .filter(filter_obj)
             .distinct()
             .order_by(order_by))

    if kwargs.get('count_model'):
        query = query.annotate(num_items=Count(kwargs.get('count_model')))

    return query


def get_or_create_term(taxonomy, title):
    """Get or create a taxonomy term based on a slugified title."""
    slug = slugify(title, allow_unicode=True)

    term = (taxonomy.objects
            .filter(slug=slug)
            .first()
            )

    if term:
        return term

    term = taxonomy(
        title=capfirst(title),
        slug=slugify(title, allow_unicode=True)
    )
    term.save()

    return term
