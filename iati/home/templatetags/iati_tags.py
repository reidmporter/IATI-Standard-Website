from django import template
from django.conf import settings
from home.models import HomePage
from about.models import AboutPage
from contact.models import ContactPage
from events.models import EventIndexPage, EventType, FeaturedEvent
from guidance_and_support.models import GuidanceAndSupportPage
from news.models import NewsIndexPage
from wagtail_modeltranslation.contextlib import use_language
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from django.utils import timezone
from django.template.defaultfilters import date as _date


register = template.Library()


@register.simple_tag(takes_context=True)
def default_page_url(context, default_page_name="home"):
    """Return the relative url for a top-level default page.

    Todo:
        Decide whether or not to check for contexts without request attributes.
        During pytests, if you don't mark a test to ignore template errors iati_tags will cause failures.

    """
    page_model_names = {
        'home': HomePage,
        'about': AboutPage,
        'contact': ContactPage,
        'events': EventIndexPage,
        'guidance_and_support': GuidanceAndSupportPage,
        'news': NewsIndexPage,
    }

    default_page = page_model_names[default_page_name].objects.live().first()

    if default_page is None:
        return ''
    if not hasattr(context, 'request'):
        return ''
    return default_page.get_url(context['request'])


@register.inclusion_tag("home/includes/translation_links.html", takes_context=True)
def translation_links(context, calling_page):
    """Take the inclusion template 'translation_links.html' and return a snippet of HTML with links to the requesting page in all offered languages."""
    language_results = []
    for language_code, language_name in settings.ACTIVE_LANGUAGES:
        with use_language(language_code):
            if hasattr(context, 'url'):
                language_url = pageurl(context, calling_page)
                language_results.append({"code": language_code, "name": language_name, "url": language_url})

    return {
        'languages': language_results,
    }


@register.filter
def haspassed(value):
    """Takes a date and tells you if it's in the past"""
    now = timezone.now()
    return value < now


@register.filter
def twopartdate(date_start, date_end):
    """Takes two datetimes and determines whether to display start and end times, or start and end dates.

    If an end date exists, we can compare the two dates.
    If the two dates are the same, localize the date for the first part and stringify the time range for the second.
    If the two dates are not the same, part 2 becomes the second date.

    If no end date exists, part 2 is just the start time.

    """
    part1 = _date(date_start, "DATE_FORMAT")
    enDash = u'\u2013'
    if date_end:
        if date_start.date() == date_end.date():
            part2 = "{0}{1}{2}".format(_date(date_start, "TIME_FORMAT"), enDash, _date(date_end, "TIME_FORMAT"))
            part2_is_time = True
        else:
            part2 = _date(date_end, "DATE_FORMAT")
            part2_is_time = False
    else:
        part2 = _date(date_start, "TIME_FORMAT")
        part2_is_time = True
    return {"part1": part1, "part2": part2, "part2_is_time": part2_is_time}


@register.filter
def event_type_verbose(event_type_slug):
    """Returns the localized event type name given a slug"""
    return EventType.objects.get(slug=event_type_slug).name


def discover_tree_recursive(current_page, calling_page):
    """Return the 'section sub-menu' page hierarchy from the point-of-view of the `calling_page`, to the top of the main section.
    A recursive function that discovers children if the current page is an ancestor of the page we want to draw the hierarchy to.

    Args:
        current_page (Page): At any given level of recursion, the page which we're trying to relate to calling_page.
        At the first level, this starts at a main section, like the About Page, and follows the hierarchy down pages that are valid ancestors of calling_page.
        calling_page (Page): The page where the side-panel will appear.

    Returns:
        list of dict: Flat list of dictionaries (each containing information about the page) that allows the template to draw the menu linearly, rather than hierarchically
    """
    parent_menu = []
    for child in current_page.get_children().live().specific():
        page_dict = {
            'page_title': child.heading if child.heading else child.title,
            'page_slug': child.slug,
            'page_depth': child.depth,
            'is_active': (child in calling_page.get_ancestors().specific()) or (child == calling_page)
        }
        parent_menu.append(page_dict)
        if page_dict['is_active']:
            child_menu = discover_tree_recursive(child, calling_page)
            parent_menu = parent_menu + child_menu
    return parent_menu


@register.inclusion_tag('home/includes/sidepanel.html')
def side_panel(calling_page):
    """Return the side panel given the page hierarchy."""
    if calling_page.depth <= 3:  # If the page where this is called is already a main section of the site (e.g. About page)
        main_section = calling_page
    else:
        home_page = HomePage.objects.live().first()
        main_section = home_page.get_children().ancestor_of(calling_page).live().first().specific

    menu_to_display = discover_tree_recursive(main_section, calling_page)
    return {"menu_to_display": menu_to_display}


@register.inclusion_tag('home/includes/featured_event.html')
def featured_events():
    """Return the featured event markup for upcoming featured events."""
    now = timezone.now()
    return {"featured_events": FeaturedEvent.objects.filter(event__live=True, event__date_start__gte=now)}
