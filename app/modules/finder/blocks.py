from wagtail.contrib.table_block.blocks import TableBlock
import logging

"""Docs for underlying TableBlock:
https://docs.wagtail.io/en/stable/reference/contrib/table_block.html
"""


class FinderBlock(TableBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_options["minSpareRows"] = 1
        self.table_options["startCols"] = 4
        self.table_options["autoColumnSize"] = True

    class Meta:
        template = "finder/blocks/finder_block.html"
