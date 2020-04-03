def assert_rich_text(rendered):
    '<div class="block-rich_text">' in rendered
    assert 'Nullam quis risus eget' in rendered


RICHTEXT_BLOCK = {
    'type': 'rich_text',
    'value': """Nullam quis risus eget urna mollis ornare vel eu leo. Morbi leo risus, porta ac
    consectetur ac, vestibulum at eros. Integer posuere erat a ante venenatis dapibus posuere velit
    aliquet. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum
    massa justo sit amet risus. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Cras
    justo odio, dapibus ac facilisis in, egestas eget quam. Nullam quis risus eget urna mollis
    ornare vel eu leo."""
}


PROMO_BLOCK = {
    "type": "promo",
    "value": {
        "url": "http://example.com/",
        "heading": "A promo",
        "description": "This is a promo block with no image.",
        "content_image": None,
        "alt_text": "",
        "size": "",
        "heading_level": 3
    }
}

SMALL_PROMO = {
    "type": "promo",
    "value": {
        "url": "http://example.com/",
        "heading": "Small promo",
        "description": "This promo uses the 'small' size variant",
        "content_image": None,
        "alt_text": "",
        "size": "small",
        "heading_level": 3
    }
}

PROMO_GROUP = {
    "type": "promo_group",
    "value": {
        "column": "one-third",
        "size": "",
        "heading_level": 3,
        "promos": [
            {
                "url": "http://example.com/",
                "heading": "Promo group item 1",
                "description": "",
                "content_image": 1, "alt_text": ""
            }, {
                "url": "http://example.com/",
                "heading": "Promo group item 2",
                "description": "A promo can have description text instead of an image",
                "content_image": None,
                "alt_text": ""
            }, {
                "url": "http://example.com/",
                "heading": "Promo group item 3",
                "description": "",
                "content_image": None,
                "alt_text": ""
            }, {
                "url": "http://example.com/",
                "heading": "Promo group item 4",
                "description": "The 4th item wraps into a new row",
                "content_image": None,
                "alt_text": ""
            }
        ]
    }
}
