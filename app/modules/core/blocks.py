# 3rd party
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock

from wagtailnhsukfrontend.blocks import (  # NOQA
    ImageBlock, PanelBlock, PromoBlock, ExpanderBlock, GreyPanelBlock, InsetTextBlock,
    PanelListBlock, PromoGroupBlock, WarningCalloutBlock
)

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
]

nhsx_blocks = content_blocks + nhs_blocks
