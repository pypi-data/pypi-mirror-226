from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.http import QueryDict
from django.utils.translation import gettext_lazy, pgettext_lazy
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class Publication(CMSPlugin):
    title = models.CharField(verbose_name=gettext_lazy("Title"), max_length=250)
    url = models.URLField(
        verbose_name=gettext_lazy("URL"),
        help_text=gettext_lazy("The URL of the publication"),
    )

    MODE_CHOICES = (
        ("mini", gettext_lazy("Mini")),
        ("viewer", pgettext_lazy("like a book", "Publication")),
    )
    mode = models.CharField(
        verbose_name=gettext_lazy("Mode"),
        choices=MODE_CHOICES,
        max_length=6,
        default=MODE_CHOICES[0][0],
    )

    VIEW_CHOICES = (
        ("", gettext_lazy("Auto")),
        ("book", pgettext_lazy("noun", "Book")),
        ("slide", gettext_lazy("Slide")),
        ("scroll", gettext_lazy("Scroll")),
    )
    view = models.CharField(
        verbose_name=gettext_lazy("View"),
        choices=VIEW_CHOICES,
        max_length=6,
        blank=True,
        default=VIEW_CHOICES[0][0],
    )

    SIZE_CHOICES = (
        ("small", gettext_lazy("Small")),
        ("medium", gettext_lazy("Medium")),
        ("big", gettext_lazy("Big")),
        ("full", gettext_lazy("Full")),
    )
    size = models.CharField(
        verbose_name=gettext_lazy("Size"),
        choices=SIZE_CHOICES,
        max_length=6,
        default=SIZE_CHOICES[1][0],
    )

    default_page = models.IntegerField(
        verbose_name=gettext_lazy("Default page"),
        default=1,
        help_text=gettext_lazy("Enter the page number to display by default"),
    )

    ACTIONS_CHOICES = (
        ("embed", gettext_lazy("Open publication in full screen directly")),
        ("public", gettext_lazy("Open description page")),
        ("view", gettext_lazy("Open viewer directly")),
    )
    actions = models.CharField(
        verbose_name=gettext_lazy("Actions"),
        choices=ACTIONS_CHOICES,
        max_length=6,
        default=ACTIONS_CHOICES[0][0],
    )

    must_open_in_new_window = models.BooleanField(
        gettext_lazy("Open in new window"), default=True
    )
    must_show_share_menu = models.BooleanField(
        gettext_lazy("Show the sharing menu after reading"), default=True
    )
    must_show_book_title = models.BooleanField(
        gettext_lazy("Display the publication title"), default=True
    )
    must_auto_flip = models.BooleanField(
        gettext_lazy("Automatically turn pages"), default=False
    )

    class Meta:
        verbose_name = gettext_lazy("Publication")
        verbose_name_plural = gettext_lazy("Publications")

    def __str__(self):
        return self.title

    @property
    def code(self):
        "Return the publication code parsed from the URL"
        return self.url.rstrip("/").split("/")[-1]

    def get_size(self):
        if self.size == self.SIZE_CHOICES[0][0]:
            return {"width": "400", "height": "250"}
        elif self.size == self.SIZE_CHOICES[1][0]:
            return {"width": "480", "height": "300"}
        elif self.size == self.SIZE_CHOICES[2][0]:
            return {"width": "560", "height": "350"}
        else:
            return {"width": "100%", "height": "100%"}

    def get_parameters(self):
        parameters = QueryDict(mutable=True)
        parameters["bkcode"] = self.code
        parameters["mode"] = self.mode
        if self.view != "":
            parameters["view"] = self.view
        parameters["page"] = self.default_page
        parameters["clickto"] = self.actions
        parameters["clicktarget"] = (
            "_blank" if self.must_open_in_new_window else "_self"
        )
        parameters["showsharemenu"] = self.must_show_share_menu
        if self.must_auto_flip:
            parameters["autoflip"] = 4

        return parameters.urlencode()
