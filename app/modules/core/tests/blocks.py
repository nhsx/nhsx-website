def assert_rich_text(rendered):
    assert '<div class="block-rich_text">' in rendered
    assert 'Nullam quis risus eget' in rendered


def assert_promo(rendered):
    assert "This is a promo block with no image." in rendered
    assert '<p class="nhsuk-promo__description">' in rendered


def assert_small_promo(rendered):
    assert 'nhsuk-promo nhsuk-promo--small' in rendered
    assert '<p class="nhsuk-promo__description">' in rendered
    assert "This promo uses the small size variant" in rendered


RICHTEXT_BLOCK = {
    'type': 'rich_text',
    'value': """Nullam quis risus eget urna mollis ornare vel eu leo. Morbi leo risus, porta ac
    consectetur ac, vestibulum at eros. Integer posuere erat a ante venenatis dapibus posuere velit
    aliquet. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum
    massa justo sit amet risus. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Cras
    justo odio, dapibus ac facilisis in, egestas eget quam. Nullam quis risus eget urna mollis
    ornare vel eu leo."""
}


PROMO = {
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
        "description": "This promo uses the small size variant",
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


ACTION_LINK = {
    "type": "action_link",
    "value": {
        "text": "Action Link",
        "external_url":
        "https://example.com",
        "new_window": False
    }
},

CARE_CARD = {
    "type": "care_card",
    "value": {
        "type": "primary",
        "heading_level": 3,
        "title": "Non-urgent:",
        "body": [
            {
                "type": "richtext",
                "value": "<p>This is a primary care card</p>"
            },
            {
                "type": "warning_callout",
                "value": {
                    "title": "Important",
                    "heading_level": 3,
                    "body": "<p>Care cards can contain other blocks</p>"
                }
            }
        ]
    }
}

CARE_CARD_2 = {
    "type": "care_card",
    "value": {
        "type": "urgent",
        "heading_level": 3,
        "title": "Urgent:",
        "body": [
            {
                "type": "richtext",
                "value": "<p>This is an urgent care card</p>"
            }
        ]
    }
}

CARE_CARD_3 = {
    "type": "care_card",
    "value": {
        "type": "immediate",
        "heading_level": 3,
        "title": "Immediate!",
        "body": [
            {
                "type": "richtext",
                "value": "<p>This is an immediate care card</p>"
            }
        ]
    }
}

DETAILS = {
    "type": "details",
    "value": {
        "title": "Details",
        "body": [
            {
                "type": "richtext",
                "value": """<p>Make a page easier to scan by letting users reveal more detailed
                information only if they need it.</p>"""
            },
            {
                "type": "panel",
                "value": {
                    "label": "Panel inside details",
                    "heading_level": 3,
                    "body": "<p>Details can contain sub blocks too</p>"
                }
            }
        ]
    }
}

DO_LIST = {
    "type": "do_list",
    "value": {
        "heading_level": 3,
        "do": [
            "<p>Do be good</p>",
            "<p>Do be happy</p>",
            "<p>Do be early</p>",
            "<p>Always eat what&#x27;s on your plate</p>"
        ]
    }
}

DONT_LIST = {
    "type": "dont_list",
    "value": {
        "heading_level": 3,
        "dont": [
            "<p>Don&#x27;t be bad</p>",
            "<p>Don&#x27;t be sad</p>",
            "<p>Don&#x27;t be late</p>"
        ]
    }
}

EXPANDER = {
    "type": "expander",
    "value": {
        "title": "Expander",
        "body": [
            {
                "type": "richtext",
                "value": """<p>Make a complex topic easier to digest by letting users reveal more
                detailed information only if they need it.</p>"""
            }
        ]
    }
},

EXPANDER_GROUP = {
    "type": "expander_group",
    "value": {
        "expanders": [
            {
                "title": "One",
                "body": [
                    {
                        "type": "richtext",
                        "value": "<p>First expander</p>"
                    }
                ]
            },
            {
                "title": "Two",
                "body": [
                    {
                        "type": "richtext",
                        "value": "<p>Second expander</p>"
                    }
                ]
            },
            {
                "title": "Three",
                "body": [
                    {
                        "type": "richtext",
                        "value": "<p>Third expander</p>"
                    }
                ]
            }
        ]
    }
}

INSET_TEXT = {
    "type": "inset_text",
    "value": {
        "body": """<p>Use inset text to help users identify and understand important content on the
        page, even if they don&#x27;t read the whole page.</p>"""
    }
}

IMAGE = {
    "type": "image",
    "value": {
        "content_image": 1,
        "alt_text": """The BBC test card. A girl playing naughts and crosses on a blackboard with a
        clown doll""",
        "caption": "BBC test card F"
    }
}

PANEL = {
    "type": "panel",
    "value": {
        "label": "Panel",
        "heading_level": 3,
        "body": "<p>Panel with a blue title</p>"
    }
}

PANEL_2 = {
    "type": "panel",
    "value": {
        "label": "",
        "heading_level": 3,
        "body": "<p>Panels don&#x27;t require a title</p>"
    }
}

WARNING_CALLOUT = {
    "type": "warning_callout",
    "value": {
        "title": "Important",
        "heading_level": 3,
        "body": "<p>This is a warning callout box! It contains <b>RichText</b></p>"
    }
}

SUMMARY_LIST = {
    "type": "summary_list",
    "value": {
        "rows": [
            {
                "key": "Name",
                "value": "<p>Sarah Philips</p>"
            },
            {
                "key": "Date of birth",
                "value": "<p>5 January 1978</p>"
            },
            {
                "key": "Contact information",
                "value": "<p>72 Guild Street<br/>London<br/>SE23 6FH</p>"
            }
        ],
        "no_border": False
    }
}

LINK_BLOCK = {
    "type": "link",
    "value": {
        "label": "Foo",
        "link": {
            "link_external": "http://example.com"
        }
    }
}

