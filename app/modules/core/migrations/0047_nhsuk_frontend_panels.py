from django.db import migrations
from modules.publications.models import PublicationPage
from wagtailnhsukfrontend.blocks import CardFeatureBlock
from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.blocks.struct_block import StructValue
import copy
import json
from wagtail.core.models import PageRevision

# Transformation documentation:
# https://github.com/nhsuk/wagtail-nhsuk-frontend/blob/master/CHANGELOG.md#v100
# With great thanks to Andy Babic for explaining how to migrate
# https://wagtailcms.slack.com/archives/C81FGJR2S/p1658748123806079

def card_group(data):
    """{'type': 'card_group', 'value': {'column': 'one-half', 'body': [
        {'type': 'card_image',
         'value': {
             'heading': 'cardwithimage',
             'heading_level': 3,
             'heading_size': '',
             'body': '',
             'content_image': 1,
             'alt_text': 'card with image',
             'url': 'http://kittenwar.com',
             'internal_page': None},
        'id': 'c9921c84-bf66-44dc-960e-a671d7080412'}]}, 'id': '0ac8c8c9-ef6d-434e-8954-b2333193539d'}"""
    print (data)
    breakpoint()
    return data

def promo_group(data):
    """{'type': 'promo_group', 'value': {'column': 'one-half', 'size': '', 'heading_level': 3,
        'promos': [
            {'link_page': 3, 'url': '', 'heading': 'promogroup promo h',
            'description': 'promo d', 'content_image': 1, 'alt_text': 'alt promo'}
        ]}, 'id': 'bbe1e442-0f77-4929-8cba-46075fda1266'}"""
    breakpoint()
    promos = data['value']['promos']
    heading_level = data['value']['heading_level']
    for p in promos:
        p['internal_page'] = p['link_page']
        p['body'] = p['description']
        p['heading_level'] = heading_level
        del(p['link_page'])
        del(p['description'])
    bodies = [{
        'type': 'card_image',
        'value': promo}
        for promo in promos]
    data = {
        'type': 'card_group',
        'value': {'column': 'one-half', 'body': bodies},
    }
    return(data)

def panel_list(data):
    panel_data = data['value']['panels']
    panels = []
    for panel in panel_data:
        panels.append(panel['left_panel'])
        panels.append(panel['right_panel'])
    breakpoint()
    bodies = [{
        'type': 'card_basic',
        'value': {'heading': panel['label'],
                  'heading_level': panel['heading_level'],
                  'heading_size': '',
                  'body': panel['body'],
        },
        #  'id': 'pidiojwdoijwijio'
    } for panel in panels]

    data = {
        'type': 'card_group',
        'value': {'column': 'one-half', 'body': bodies},
    }
    print(data)
    breakpoint()
    return(data)

def panel(data):
    new_data = copy.deepcopy(data)
    new_data['type'] = 'card_feature'
    value = new_data['value']
    value['feature_heading'] = value['label']
    del(value['label'])
    return new_data

def promo(data):
    # image, alt text required; just causes a validation error on save
    # so that's OK.
    new_data = copy.deepcopy(data)
    new_data['type'] = 'card_image'
    value = new_data['value']
    value['body'] = value['description']
    value['heading_size'] = value['size']
    value['internal_page'] = value['link_page']  # not documented! TODO
    del(value['description'])
    del(value['size'])
    del(value['link_page'])
    return new_data
    # 'link_page': 3, 'url': ''
    # 'url': 'http://url.com', 'internal_page': None

forward_mapper = {
    'grey_panel': panel,
    'panel': panel,
    'promo': promo,
    'panel_list': panel_list,
    'promo_group': promo_group,
    'card_group': card_group,

}

def alter_raw_data(page, mapper):
    mapped = False
    new_data = []
    for block_data in page.body.raw_data:
        block_type = block_data['type']
        if block_type in mapper:
            new_data.append(mapper[block_type](block_data))
            mapped = True
        else:
            new_data.append(block_data)
    return json.dumps(new_data), mapped

def migrate(apps, mapper):
    for page in PublicationPage.objects.all():
        stream_data, mapped = alter_raw_data(page, mapper)

        if mapped:
            page.body = stream_data
            page.save()
            PageRevision.objects.filter(page_id=page.id).delete()
    print ("DONE")
    breakpoint()
    # raise RuntimeError()

def forwards(apps, schema_editor):
    migrate(apps, forward_mapper)

def backwards(*args, **kwargs):
    raise NotImplementedError("Forwards only")

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20210902_1250'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
