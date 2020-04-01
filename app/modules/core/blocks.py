# 3rd party
from wagtailnhsukfrontend.blocks import (  # NOQA
    ImageBlock, PanelBlock, PromoBlock, ExpanderBlock, GreyPanelBlock, InsetTextBlock,
    PanelListBlock, PromoGroupBlock, WarningCalloutBlock
)


nhsx_blocks = [
    ('image_block', ImageBlock()),
    ('panel_block', PanelBlock()),
    ('promo_block', PromoBlock()),
    ('expander_block', ExpanderBlock()),
    ('grey_panel_block', GreyPanelBlock()),
    ('inset_text_block', InsetTextBlock()),
    ('panel_list_block', PanelListBlock()),
    ('promo_group_block', PromoGroupBlock()),
    ('warning_callout_block', WarningCalloutBlock()),
]
