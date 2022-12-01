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

"""
from modules.meeting_minutes.models import  MeetingMinutes, MeetingMinutesListingPage
from modules.home.models import HomePage
from modules.blog_posts.models import BlogPost, BlogPostIndexPage
from modules.core.models.pages import SectionPage, ArticlePage, CookieFormPage
# mixin may be off on on the next line
from modules.ai_lab.models.resource_listings import AiLabResourceCollection, AiLabResourceIndexPage, AiLabCategoryIndexPageMixin
from modules.ai_lab.models.resources import AiLabCaseStudy, AiLabGuidance, AiLabReport, AiLabExternalResource, AiLabInternalResource
# core pages may be incorrect
from modules.core.models.abstract import BasePage, BaseIndexPage
from modules.publications.models import PublicationPage, PublicationIndexPage
from modules.news.models import News, NewsIndexPage
from modules.people.models import Person, PeopleListingPage
# Template may be wrong
from modules.ig_guidance.models import IGGuidance, GuidanceListingPage, InternalGuidance, ExternalGuidance, IGTemplate
from modules.case_studies. models import CaseStudyPage
"""

"""
all_page_types = [
   # MeetingMinutes -- no body
   MeetingMinutesListingPage,
HomePage,
 BlogPost, BlogPostIndexPage,
 SectionPage, ArticlePage, CookieFormPage,
 AiLabResourceCollection, AiLabResourceIndexPage,
 # AiLabCategoryIndexPageMixin -- abstract
 AiLabCaseStudy, AiLabGuidance, AiLabReport,
 # AiLabExternalResource, AiLabInternalResource, -- no body
 # BasePage,  BaseIndexPage,-- abstract

 PublicationPage, PublicationIndexPage,
 News, NewsIndexPage,
 Person, PeopleListingPage,
 # IGGuidance,  -- abstract
 GuidanceListingPage, InternalGuidance, ExternalGuidance, IGTemplate,
 CaseStudyPage,

]
"""



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
    return data

def promo_group(data):
    """{'type': 'promo_group', 'value': {'column': 'one-half', 'size': '', 'heading_level': 3,
        'promos': [
            {'link_page': 3, 'url': '', 'heading': 'promogroup promo h',
            'description': 'promo d', 'content_image': 1, 'alt_text': 'alt promo'}
        ]}, 'id': 'bbe1e442-0f77-4929-8cba-46075fda1266'}"""
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
    for page_type in all_page_types:
        print(f"Starting {page_type.__name__}...")
        for page in page_type.objects.all():
            print(f"Considering {page_type.__name__}: '{page}'")
            stream_data, mapped = alter_raw_data(page, mapper)

            if mapped:
                print(f"Modified {page_type.__name__} '{page}'")
                page.body = stream_data
                page.save()
                PageRevision.objects.filter(page_id=page.id).delete()
        print (f"That was the last {page_type.__name__}")

def forwards(apps, schema_editor):
    migrate(apps, forward_mapper)

def backwards(*args, **kwargs):
    raise NotImplementedError("Forwards only")

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20210902_1250'),
    ]
'''
    operations = [
        migrations.RunPython(forwards, backwards)
    ]
'''
