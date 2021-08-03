# Generated by Django 3.2.5 on 2021-08-02 15:55

from django.db import migrations
import modules.core.blocks
import modules.core.models.snippets
import modules.finder.blocks
import wagtail.core.blocks
import wagtail.core.blocks.field_block
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.snippets.blocks
import wagtailnhsukfrontend.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('case_studies', '0007_alter_casestudypage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casestudypage',
            name='body',
            field=wagtail.core.fields.StreamField([('rich_text', wagtail.core.blocks.RichTextBlock(group=' Content')), ('block_quote', wagtail.core.blocks.BlockQuoteBlock(group=' Content')), ('embed', modules.core.blocks.EmbedBlock(group=' Content')), ('captioned_embed', wagtail.core.blocks.StructBlock([('embed', modules.core.blocks.EmbedBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('sub_title', wagtail.core.blocks.CharBlock(required=False))], group=' Content')), ('html_anchor', wagtail.core.blocks.StructBlock([('anchor', wagtail.core.blocks.CharBlock(help_text="Some where in the page you will need to add the anchor link to this ID. e.g. Use the 'rich text' block to add the anchor link", label='ID for anchor'))], group=' Content')), ('image', wagtail.core.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False))], group=' NHS Components')), ('expander', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('body', wagtail.core.blocks.StreamBlock([('richtext', wagtail.core.blocks.RichTextBlock()), ('action_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('inset_text', wagtail.core.blocks.StructBlock([('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('image', wagtail.core.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('grey_panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(label='heading', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no heading. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('feature_card', wagtail.core.blocks.StructBlock([('feature_heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.core.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.core.blocks.StructBlock([('rows', wagtail.core.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('table', modules.core.blocks.TableBlock())], required=True))], group=' NHS Components')), ('inset_text', wagtail.core.blocks.StructBlock([('body', wagtail.core.blocks.RichTextBlock(required=True))], group=' NHS Components')), ('warning_callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.core.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.core.blocks.RichTextBlock(required=True))], group=' NHS Components')), ('table', modules.core.blocks.TableBlock(group=' NHS Components')), ('panel_table', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('table', modules.core.blocks.TableBlock())], group=' NHS Components')), ('action_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Internal Page', required=False))], group=' NHS Components')), ('legal_information', wagtail.core.blocks.StructBlock([('legal_information', wagtail.snippets.blocks.SnippetChooserBlock(modules.core.models.snippets.LegalInformation))], group=' NHS Components')), ('newsletter_signup', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.', max_value=4, min_value=2)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('mailing_list_id', wagtail.core.blocks.CharBlock(required=True))], group=' Content')), ('finder', modules.finder.blocks.FinderBlock(group=' NHS Components')), ('care_card', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('primary', 'Non-urgent'), ('urgent', 'Urgent'), ('immediate', 'Immediate')])), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.', max_value=6, min_value=2, required=True)), ('title', wagtail.core.blocks.CharBlock(required=True)), ('body', wagtail.core.blocks.StreamBlock([('richtext', wagtail.core.blocks.RichTextBlock()), ('action_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('details', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('body', wagtail.core.blocks.StreamBlock([('richtext', wagtail.core.blocks.RichTextBlock()), ('action_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('inset_text', wagtail.core.blocks.StructBlock([('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('image', wagtail.core.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('feature_card', wagtail.core.blocks.StructBlock([('feature_heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.core.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.core.blocks.StructBlock([('rows', wagtail.core.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.core.blocks.BooleanBlock(default=False, required=False))]))], required=True))])), ('inset_text', wagtail.core.blocks.StructBlock([('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('image', wagtail.core.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('grey_panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(label='heading', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no heading. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('feature_card', wagtail.core.blocks.StructBlock([('feature_heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.core.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.core.blocks.StructBlock([('rows', wagtail.core.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.core.blocks.BooleanBlock(default=False, required=False))]))], required=True))], group=' NHS Components')), ('expander_group', wagtail.core.blocks.StructBlock([('expanders', wagtail.core.blocks.ListBlock(wagtailnhsukfrontend.blocks.ExpanderBlock))], group=' NHS Components')), ('details', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('body', wagtail.core.blocks.StreamBlock([('richtext', wagtail.core.blocks.RichTextBlock()), ('action_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('inset_text', wagtail.core.blocks.StructBlock([('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('image', wagtail.core.blocks.StructBlock([('content_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Only leave this blank if the image is decorative.', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('feature_card', wagtail.core.blocks.StructBlock([('feature_heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('warning_callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.core.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('summary_list', wagtail.core.blocks.StructBlock([('rows', wagtail.core.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.core.blocks.BooleanBlock(default=False, required=False))]))], required=True))], group=' NHS Components')), ('card_group', wagtail.core.blocks.StructBlock([('column', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.core.blocks.StreamBlock([('card_basic', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.core.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(required=True)), ('url', wagtail.core.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.core.blocks.StructBlock([('feature_heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=True))]))], required=True))], group=' NHS Components')), ('card_feature', wagtail.core.blocks.StructBlock([('feature_heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=True))], group=' NHS Components')), ('card_image', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(required=True)), ('url', wagtail.core.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))], group=' NHS Components')), ('card_clickable', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.core.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))], group=' NHS Components')), ('card_basic', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=True)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.core.blocks.RichTextBlock(required=False))], group=' NHS Components')), ('summary_list', wagtail.core.blocks.StructBlock([('rows', wagtail.core.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.core.blocks.BooleanBlock(default=False, required=False))], group=' NHS Components')), ('summary_list_row', wagtail.core.blocks.StructBlock([('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.RichTextBlock())], group=' NHS Components')), ('dont', wagtail.core.blocks.StructBlock([('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('label', wagtail.core.blocks.CharBlock(help_text="Adding a label here will overwrite the default of Don't", label='Heading', required=False)), ('dont', wagtail.core.blocks.ListBlock(wagtail.core.blocks.field_block.RichTextBlock, label="Don't"))], group=' NHS Components')), ('do', wagtail.core.blocks.StructBlock([('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('label', wagtail.core.blocks.CharBlock(help_text='Adding a label here will overwrite the default of Do', label='Heading', required=False)), ('do', wagtail.core.blocks.ListBlock(wagtail.core.blocks.field_block.RichTextBlock))], group=' NHS Components')), ('grey_panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(label='heading', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no heading. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))], group='Deprecated')), ('panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))], group='Deprecated')), ('panel_list', wagtail.core.blocks.StructBlock([('panels', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('left_panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))])), ('right_panel', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock(required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('body', wagtail.core.blocks.RichTextBlock(required=True))]))])))], group='Deprecated')), ('promo', wagtail.core.blocks.StructBlock([('link_page', wagtail.core.blocks.PageChooserBlock(label='Page', required=False)), ('url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('heading', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=False)), ('alt_text', wagtail.core.blocks.CharBlock(required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small')], required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.', max_value=4, min_value=2))], group='Deprecated')), ('promo_group', wagtail.core.blocks.StructBlock([('column', wagtail.core.blocks.ChoiceBlock(choices=[('one-half', 'One-half'), ('one-third', 'One-third')])), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small')], required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=4.', max_value=4, min_value=2)), ('promos', wagtail.core.blocks.ListBlock(modules.core.blocks.BasePromoBlock))], group='Deprecated'))], blank=True, verbose_name='Body blocks'),
        ),
    ]