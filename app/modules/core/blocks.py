# 3rd party
import collections

from bs4 import BeautifulSoup

from wagtail.core import blocks
from wagtail.embeds import embeds
from wagtail.embeds.blocks import EmbedBlock as WagtailEmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock as OGTableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from taggit.models import Tag

from wagtailnhsukfrontend.blocks import (  # NOQA
    ImageBlock,
    PanelBlock,
    ExpanderBlock,
    GreyPanelBlock,  # deprecated, not in v5 (0.8)
    InsetTextBlock,
    PanelListBlock,  # deprecated, not in v5 (0.8)
    WarningCalloutBlock,
    FlattenValueContext,
    ActionLinkBlock,
    # below here appear new to v5 (0.7+)
    CareCardBlock,
    ExpanderGroupBlock,
    DetailsBlock,
    CardGroupBlock,
    CardFeatureBlock,
    CardImageBlock,
    CardClickableBlock,
    CardBasicBlock,
    SummaryListBlock,
    SummaryListRowBlock,
    BasePromoBlock,
    DontBlock,
    DoBlock,
)

# Project specific Models
from modules.core.models.snippets import LegalInformation
from modules.finder.blocks import FinderBlock

from modules.case_studies.abstract import (
    CaseStudyTag,
    CaseStudyTags,
)


class BasePromoBlock(FlattenValueContext, blocks.StructBlock):
    class Meta:
        icon = "pick"
        template = "wagtailnhsukfrontend/promo.html"

    link_page = blocks.PageChooserBlock(required=False, label="Page")
    url = blocks.URLBlock(label="URL", required=False)
    heading = blocks.CharBlock(required=True)
    description = blocks.CharBlock(required=False)
    content_image = ImageChooserBlock(label="Image", required=False)
    alt_text = blocks.CharBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        page = value.get("link_page", "")
        if page is not None:
            url = page.url
        else:
            url = value.get("url", "")

        context["url"] = url
        return context


class PromoBlock(BasePromoBlock):
    class Meta:
        template = "wagtailnhsukfrontend/promo.html"

    size = blocks.ChoiceBlock(
        [
            ("", "Default"),
            ("small", "Small"),
        ],
        required=False,
    )

    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text="The heading level affects users with screen readers. Default=3, Min=2, Max=4.",
    )


class PromoBanner(BasePromoBlock):
    class Meta:
        template = "core/blocks/promo_banner.html"

    call_to_action = blocks.CharBlock(required=True)
    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text="The heading level affects users with screen readers. Default=3, Min=2, Max=4.",
    )
    image_alignment = blocks.ChoiceBlock(
        [
            ("right", "Right"),
            ("left", "Left"),
        ],
        default="right",
        required=True,
    )

    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)
        # Alter the order of the form, so it makes more sense
        new_keys = [
            "heading",
            "heading_level",
            "description",
            "link_page",
            "url",
            "call_to_action",
            "content_image",
            "alt_text",
            "image_alignment",
        ]
        form_objects = collections.OrderedDict()
        for key in new_keys:
            form_objects[key] = context["children"][key]

        context["children"] = form_objects
        return context


class PromoGroupBlock(FlattenValueContext, blocks.StructBlock):
    class Meta:
        template = "wagtailnhsukfrontend/promo_group.html"

    column = blocks.ChoiceBlock(
        [
            ("one-half", "One-half"),
            ("one-third", "One-third"),
        ],
        default="one-half",
        required=True,
    )

    size = blocks.ChoiceBlock(
        [
            ("", "Default"),
            ("small", "Small"),
        ],
        required=False,
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["num_columns"] = {
            "one-half": 2,
            "one-third": 3,
        }[value["column"]]
        return context

    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text="The heading level affects users with screen readers. Default=3, Min=2, Max=4.",
    )

    promos = blocks.ListBlock(BasePromoBlock)


class StepBlock(FlattenValueContext, blocks.StructBlock):
    class Meta:
        icon = "pick"
        template = "core/blocks/step.html"

    heading = blocks.CharBlock(required=True)
    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=2,
        help_text="The heading level affects users with screen readers. Default=2, Min=2, Max=4.",
    )
    body = blocks.RichTextBlock(required=False)


class StepGroupBlock(FlattenValueContext, blocks.StructBlock):
    class Meta:
        template = "core/blocks/step_group.html"

    heading = blocks.CharBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        return context

    steps = blocks.ListBlock(StepBlock)


class TableBlock(OGTableBlock):
    class Meta:
        template = "core/blocks/table.html"


class PanelTableBlock(blocks.StructBlock):
    class Meta:
        template = "core/blocks/panel_table.html"

    title = blocks.CharBlock()
    table = TableBlock()


class EmbedWithTitle:
    def fetch_from_url(self, url):
        embed = embeds.get_embed(url)

        return {
            "html": self._add_title_to_iframe(embed),
            "url": url,
            "ratio": embed.ratio,
        }

    def _add_title_to_iframe(self, embed):
        html = BeautifulSoup(embed.html, "html5lib")
        html.iframe["title"] = embed.title

        return str(html.iframe)


class EmbedBlock(WagtailEmbedBlock, EmbedWithTitle):

    """Overriding the built in Wagtail embed so that we can have proper
    responsive markup.
    """

    class Meta:
        template = "core/blocks/embed.html"

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)

        embed_url = getattr(value, "url", None)
        if embed_url:
            data = self.fetch_from_url(embed_url)
            context["embed_html"] = data["html"]
            context["embed_url"] = data["url"]
            context["ratio"] = data["ratio"]

        return context


class CaptionedEmbedBlock(blocks.StructBlock, EmbedWithTitle):

    """Overriding the built in Wagtail embed so that we can have proper
    responsive markup.
    """

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        embed_url = value["embed"].url

        if embed_url:
            data = self.fetch_from_url(embed_url)
            context["value"]["embed"].html = data["html"]

        return context

    class Meta:
        template = "core/blocks/captioned_embed.html"

    embed = EmbedBlock()
    title = blocks.CharBlock(required=False)
    sub_title = blocks.CharBlock(required=False)


class LinkStructBlockMixin(object):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        context["value"]["url"] = self.get_url(value["link"])
        return context

    def get_url(self, value):

        if value["link_page"]:
            return value["link_page"].url

        elif value["link_document"]:
            return value["link_document"].file

        elif value["link_external"]:
            return value["link_external"]

        return None


class LinkFields(blocks.StructBlock):
    link_page = blocks.PageChooserBlock(required=False, label="Page")
    link_document = DocumentChooserBlock(required=False, label="Document")
    link_external = blocks.URLBlock(required=False, label="URL")


class LinkBlock(blocks.StructBlock, LinkStructBlockMixin):
    label = blocks.CharBlock(required=False)
    link = LinkFields(required=False, label="Link to (choose one)")


class NHSXExpanderBody(ExpanderBlock.BodyStreamBlock):
    table = TableBlock()


class NHSXExpanderBlock(ExpanderBlock):
    body = NHSXExpanderBody(required=True)


def get_tag_list():
    return [(_.id, _.name) for _ in Tag.objects.all()]


def get_casestudy_tag_list():
    return [(_.id, _.name) for _ in CaseStudyTag.objects.all()]


class LatestItemBlockMixin(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    number_of_posts = blocks.ChoiceBlock(
        [(1, "One"), (2, "Two"), (3, "Three")], default=3, required=True
    )
    tag_id = blocks.ChoiceBlock(choices=get_tag_list, required=True)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        value["tag"] = Tag.objects.get(id=value["tag_id"])
        value["items"] = self._get_items(value["tag_id"], int(value["number_of_posts"]))
        context.update(value)
        return context

    class Meta:
        abstract = True


class LatestBlogPostsBlock(LatestItemBlockMixin):
    def _get_items(self, tag_id, limit):
        from modules.blog_posts.models import BlogPost

        return (
            BlogPost.objects.live()
            .filter(tags__id=tag_id)
            .live()
            .order_by("-first_published_at")
        )[:limit]

    class Meta:
        icon = "doc-full"
        template = "blocks/latest_blog_posts.html"


class LatestNewsBlock(LatestItemBlockMixin):
    def _get_items(self, tag_id, limit):
        from modules.news.models import News

        return (
            News.objects.live()
            .filter(tags__id=tag_id)
            .live()
            .order_by("-first_published_at")
        )[:limit]

    class Meta:
        icon = "doc-full"
        template = "blocks/latest_news.html"


class NewsletterBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text="The heading level affects users with screen readers. Default=3, Min=2, Max=4.",
    )

    description = blocks.CharBlock(required=False)
    mailing_list_id = blocks.CharBlock(required=True)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        return context

    class Meta:
        icon = "mail"
        template = "blocks/newsletter.html"


class CaseStudyBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text="The heading level affects users with screen readers. Default=3, Min=2, Max=4.",
    )
    column = blocks.ChoiceBlock(
        [
            ("one-half", "One-half"),
            ("one-third", "One-third"),
        ],
        default="one-third",
        required=True,
    )
    tag_id = blocks.ChoiceBlock(choices=get_casestudy_tag_list, required=True)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["num_columns"] = {
            "one-half": 2,
            "one-third": 3,
        }[value["column"]]
        value["tag"] = CaseStudyTag.objects.get(id=value["tag_id"])
        value["items"] = self._get_items(value["tag_id"], 99)
        context.update(value)
        return context

    class Meta:
        abstract = True


class CaseStudiesBlock(CaseStudyBlock):
    def _get_items(self, tag_id, limit):
        from modules.case_studies.models import CaseStudyPage

        return (
            CaseStudyPage.objects.live()
            .filter(tags__id=tag_id)
            .live()
            .order_by("display_order")
        )[:limit]

    class Meta:
        icon = "doc-full"
        template = "blocks/filtered_case_studies.html"


# Legal Information from Snippet
class LegalInformationBlock(blocks.StructBlock):

    legal_information = SnippetChooserBlock(LegalInformation)

    class Meta:
        icon = "doc-full"
        template = "core/blocks/legal_information.html"


class HTMLAnchorBlock(blocks.StructBlock):
    anchor = blocks.CharBlock(
        help_text="Some where in the page you will need to add the anchor link to this ID. e.g. Use the 'rich text' block to add the anchor link",
        label="ID for anchor",
    )

    class Meta:
        icon = "link"
        template = "core/blocks/html_anchor.html"


blog_link_blocks = [
    (
        "link",
        blocks.PageChooserBlock(
            required=True, label="Page", page_type="blog_posts.BlogPost"
        ),
    ),
]


news_link_blocks = [
    (
        "link",
        blocks.PageChooserBlock(required=True, label="Page", page_type="news.News"),
    ),
]


page_link_blocks = [
    ("link", LinkBlock()),
]


content_blocks = [
    ("rich_text", blocks.RichTextBlock(group=" Content")),
    ("block_quote", blocks.BlockQuoteBlock(group=" Content")),
    ("embed", EmbedBlock(group=" Content")),
    ("captioned_embed", CaptionedEmbedBlock(group=" Content")),
    ("html_anchor", HTMLAnchorBlock(group=" Content")),
]

deprecated_blocks = [
    ("grey_panel", GreyPanelBlock(group="Deprecated")),
    ("panel", PanelBlock(group="Deprecated")),
    ("panel_list", PanelListBlock(group="Deprecated")),
    ("promo", PromoBlock(group="Deprecated")),
    ("promo_group", PromoGroupBlock(group="Deprecated")),
]

v5_blocks = [
    ("care_card", CareCardBlock(group=" NHS Components")),
    ("expander_group", ExpanderGroupBlock(group=" NHS Components")),
    ("details", DetailsBlock(group=" NHS Components")),
    ("card_group", CardGroupBlock(group=" NHS Components")),
    ("card_feature", CardFeatureBlock(group=" NHS Components")),
    ("card_image", CardImageBlock(group=" NHS Components")),
    ("card_clickable", CardClickableBlock(group=" NHS Components")),
    ("card_basic", CardBasicBlock(group=" NHS Components")),
    ("summary_list", SummaryListBlock(group=" NHS Components")),
    ("summary_list_row", SummaryListRowBlock(group=" NHS Components")),
    ("dont", DontBlock(group=" NHS Components")),
    ("do", DoBlock(group=" NHS Components")),
]
nhs_blocks = (
    [
        ("image", ImageBlock(group=" NHS Components")),
        ("expander", NHSXExpanderBlock(group=" NHS Components")),
        ("inset_text", InsetTextBlock(group=" NHS Components")),
        ("warning_callout", WarningCalloutBlock(group=" NHS Components")),
        ("table", TableBlock(group=" NHS Components")),
        ("panel_table", PanelTableBlock(group=" NHS Components")),
        ("action_link", ActionLinkBlock(group=" NHS Components")),
        ("legal_information", LegalInformationBlock(group=" NHS Components")),
        ("newsletter_signup", NewsletterBlock(group=" Content")),
        ("finder", FinderBlock(group=" NHS Components"))
    ]
    + v5_blocks
    + deprecated_blocks
)

nhsx_blocks = content_blocks + nhs_blocks

section_page_blocks = nhsx_blocks + [
    ("latest_blog_posts", LatestBlogPostsBlock(group=" Content")),
    ("latest_news", LatestNewsBlock(group=" Content")),
    ("promo_banner", PromoBanner(group=" Content")),
    ("newsletter_signup", NewsletterBlock(group=" Content")),
    ("step_group", StepGroupBlock(group=" Content")),
    ("case_studies", CaseStudiesBlock(group=" Content")),
]
