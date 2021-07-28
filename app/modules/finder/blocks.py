from wagtail.contrib.table_block.blocks import TableBlock 
from wagtail.core.blocks import StreamBlock

"""Docs for underlying TableBlock:
https://docs.wagtail.io/en/stable/reference/contrib/table_block.html
"""

class FinderBlock(StreamBlock):

    default_table_options = {
        'minSpareRows': 1,
        'startRows': 3,
        'startCols': 4,
        'colHeaders': False,
        'rowHeaders': True,
        'contextMenu': [
            'row_above',
            'row_below',
            '---------',
            'col_left',
            'col_right',
            '---------',
            'remove_row',
            'remove_col',
            '---------',
            'undo',
            'redo'
        ],
        'editor': 'text',
        'stretchH': 'all',
        'height': 108,
        'renderer': 'text',
        'autoColumnSize': True,
    }

    table=TableBlock(table_options=default_table_options)