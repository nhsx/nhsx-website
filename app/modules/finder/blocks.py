from wagtail.contrib.table_block.blocks import TableBlock

"""Docs for underlying TableBlock:
https://docs.wagtail.io/en/stable/reference/contrib/table_block.html
"""


class FinderBlock(TableBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_options["minSpareRows"] = 1
        self.table_options["startCols"] = 4
        self.table_options["autoColumnSize"] = True

    def render(self, value, **context):
        data = value.get('data', [[]])
        offset = int(value.get('first_row_is_table_header', 0))
        # if the first row is a header, we skip it (offset=1) otherwise we don't (offset=0) 
        # and we get the second column (row[1]) and use it as a facet  
        context['context']['facets'] = list(set([row[1] for row in data[offset:]]))
        return super().render(value, **context)

    class Meta:
        template = "finder/blocks/finder_block.html"
