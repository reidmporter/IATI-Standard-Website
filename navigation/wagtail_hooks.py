from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from wagtail.core import hooks


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'navigation/js/navigation-helpers.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}"></script>', ((static(filename),) for filename in js_files))
    return js_includes


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        """
        <style>

            .custom-struct-container label
            {{
                float: none;
                width: 100%;
                display: inline-block;
            }}

            .help-text-section-header {{
                background-color: #d9d9d9;
                font-weight: 700;
                font-size: 1.2em;
            }}

        </style>
        """
    )
