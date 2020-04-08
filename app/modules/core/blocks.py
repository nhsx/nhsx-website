# 3rd party
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock as OGTableBlock

from wagtailnhsukfrontend.blocks import (  # NOQA
    ImageBlock, PanelBlock, PromoBlock, ExpanderBlock, GreyPanelBlock, InsetTextBlock,
    PanelListBlock, PromoGroupBlock, WarningCalloutBlock
)


class TableBlock(OGTableBlock):
    pass


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


page_link_blocks = [
    ('link', LinkBlock()),
]


content_blocks = [
    ('rich_text', blocks.RichTextBlock(group=" Content")),
    ('block_quote', blocks.BlockQuoteBlock(group=" Content")),
    ('embed', EmbedBlock(group=" Content")),
]

nhs_blocks = [
    ('image', ImageBlock(group=" NHS Components")),
    ('panel', PanelBlock(group=" NHS Components")),
    ('promo', PromoBlock(group=" NHS Components")),
    ('expander', ExpanderBlock(group=" NHS Components")),
    ('grey_panel', GreyPanelBlock(group=" NHS Components")),
    ('inset_text', InsetTextBlock(group=" NHS Components")),
    ('panel_list', PanelListBlock(group=" NHS Components")),
    ('promo_group', PromoGroupBlock(group=" NHS Components")),
    ('warning_callout', WarningCalloutBlock(group=" NHS Components")),
    ('table', TableBlock(group=" NHS Components")),
]

nhsx_blocks = content_blocks + nhs_blocks
