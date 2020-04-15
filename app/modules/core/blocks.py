# 3rd party
from wagtail.core import blocks
from wagtail.embeds import embeds
from wagtail.embeds.blocks import EmbedBlock as WagtailEmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock as OGTableBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtailnhsukfrontend.blocks import (  # NOQA
    ImageBlock, PanelBlock, ExpanderBlock, GreyPanelBlock, InsetTextBlock,
    PanelListBlock, WarningCalloutBlock, FlattenValueContext
)


class BasePromoBlock(FlattenValueContext, blocks.StructBlock):

    class Meta:
        icon = 'pick'
        template = 'wagtailnhsukfrontend/promo.html'

    link_page = blocks.PageChooserBlock(required=False, label="Page")
    url = blocks.URLBlock(label="URL", required=False)
    heading = blocks.CharBlock(required=True)
    description = blocks.CharBlock(required=False)
    content_image = ImageChooserBlock(label="Image", required=False)
    alt_text = blocks.CharBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        page = value.get('link_page', '')
        if page is not None:
            url = page.url
        else:
            url = value.get('url', '')

        context['url'] = url
        return context


class PromoBlock(BasePromoBlock):

    class Meta:
        template = 'wagtailnhsukfrontend/promo.html'

    size = blocks.ChoiceBlock([
        ('', 'Default'),
        ('small', 'Small'),
    ], required=False)

    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.'
    )


class PromoGroupBlock(FlattenValueContext, blocks.StructBlock):

    class Meta:
        template = 'wagtailnhsukfrontend/promo_group.html'

    column = blocks.ChoiceBlock([
        ('one-half', 'One-half'),
        ('one-third', 'One-third'),
    ], default='one-half', required=True)

    size = blocks.ChoiceBlock([
        ('', 'Default'),
        ('small', 'Small'),
    ], required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['num_columns'] = {
            'one-half': 2,
            'one-third': 3,
        }[value['column']]
        return context

    heading_level = blocks.IntegerBlock(
        min_value=2,
        max_value=4,
        default=3,
        help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.'
    )

    promos = blocks.ListBlock(BasePromoBlock)


class TableBlock(OGTableBlock):

    class Meta:
        template = 'core/blocks/table.html'


class PanelTableBlock(blocks.StructBlock):

    class Meta:
        template = 'core/blocks/panel_table.html'

    title = blocks.CharBlock()
    table = TableBlock()


class EmbedBlock(WagtailEmbedBlock):

    """Overriding the built in Wagtail embed so that we can have proper
    responsive markup.
    """

    class Meta:
        template = 'core/blocks/embed.html'

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        embed_url = getattr(value, 'url', None)
        if embed_url:
            embed = embeds.get_embed(embed_url)
            context['embed_html'] = embed.html
            context['embed_url'] = embed_url
            context['ratio'] = embed.ratio

        return context


class CaptionedEmbedBlock(blocks.StructBlock):

    """Overriding the built in Wagtail embed so that we can have proper
    responsive markup.
    """

    class Meta:
        template = 'core/blocks/captioned_embed.html'

    embed = EmbedBlock()
    title = blocks.CharBlock(required=False)
    sub_title = blocks.CharBlock(required=False)


class LinkStructBlockMixin(object):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        context['value']['url'] = self.get_url(value['link'])
        return context

    def get_url(self, value):

        if value['link_page']:
            return value['link_page'].url

        elif value['link_document']:
            return value['link_document'].file

        elif value['link_external']:
            return value['link_external']

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


blog_link_blocks = [
    ('link', blocks.PageChooserBlock(required=True, label="Page", page_type="blog_posts.BlogPost")),
]


news_link_blocks = [
    ('link', blocks.PageChooserBlock(required=True, label="Page", page_type="news.News")),
]


page_link_blocks = [
    ('link', LinkBlock()),
]


content_blocks = [
    ('rich_text', blocks.RichTextBlock(group=" Content")),
    ('block_quote', blocks.BlockQuoteBlock(group=" Content")),
    ('embed', EmbedBlock(group=" Content")),
    ('captioned_embed', CaptionedEmbedBlock(group=" Content")),
]

nhs_blocks = [
    ('image', ImageBlock(group=" NHS Components")),
    ('panel', PanelBlock(group=" NHS Components")),
    ('promo', PromoBlock(group=" NHS Components")),
    ('expander', NHSXExpanderBlock(group=" NHS Components")),
    ('grey_panel', GreyPanelBlock(group=" NHS Components")),
    ('inset_text', InsetTextBlock(group=" NHS Components")),
    ('panel_list', PanelListBlock(group=" NHS Components")),
    ('promo_group', PromoGroupBlock(group=" NHS Components")),
    ('warning_callout', WarningCalloutBlock(group=" NHS Components")),
    ('table', TableBlock(group=" NHS Components")),
    ('panel_table', PanelTableBlock(group=" NHS Components")),
]

nhsx_blocks = content_blocks + nhs_blocks
