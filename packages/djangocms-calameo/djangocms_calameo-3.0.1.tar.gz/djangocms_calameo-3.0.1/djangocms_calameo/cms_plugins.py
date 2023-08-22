from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext as _, gettext_lazy

from .models import Publication


@plugin_pool.register_plugin
class PublicationPlugin(CMSPluginBase):
    module = gettext_lazy("Widgets")
    name = gettext_lazy("Calaméo publication widget")
    model = Publication
    render_template = "djangocms_calameo/default.html"
    cache = False

    def get_fieldsets(self, request, obj):
        fieldsets = (
            (None, {"fields": ["title", "url"]}),
            (
                _("More options"),
                {
                    "classes": ("collapse",),
                    "fields": [
                        "mode",
                        "view",
                        "size",
                        "default_page",
                        "actions",
                        "must_open_in_new_window",
                        "must_show_share_menu",
                        "must_show_book_title",
                        "must_auto_flip",
                    ],
                },
            ),
        )

        return fieldsets
