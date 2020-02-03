"""Module to define a custom Multifield Panel."""

from wagtail.admin.edit_handlers import MultiFieldPanel as WagtailMultiFieldPanel
from wagtail.admin.edit_handlers import HelpPanel as WagtailHelpPanel


class MultiFieldPanel(WagtailMultiFieldPanel):
    """Class for a custom multifield panel with additional descriptions."""

    def __init__(self, children=(), *args, **kwargs):
        """Initialise the class."""
        if kwargs.get('description', None):
            self.description = kwargs.pop('description')
        super().__init__(children, *args, **kwargs)

    def clone(self):
        """Function to clone the field panel."""
        props = {
            'children': self.children,
            'heading': self.heading,
            'classname': self.classname,
            'help_text': self.help_text,
        }
        if hasattr(self, 'description'):
            props['description'] = self.description
        return self.__class__(**props)


def HelpPanel(
    content='',
    template='wagtailadmin/edit_handlers/help_panel.html',
    heading='',
    classname='',
    wrapper_class='help-block help-info'
):
    """Function for a help text panel."""
    wrapped_content = '<div class="%s">%s</div>' % (wrapper_class, content)
    return WagtailHelpPanel(content=wrapped_content, template=template, heading=heading, classname=classname)
