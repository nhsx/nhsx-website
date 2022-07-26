from wagtail import blocks


class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    organisation = blocks.CharBlock(required=True)
    role = blocks.CharBlock(required=True)
    heading = blocks.CharBlock(required=False)

    class Meta:
        icon = "user"
        template = "meeting_minutes/blocks/person.html"
