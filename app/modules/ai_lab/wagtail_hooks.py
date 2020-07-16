from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.edit_handlers import FieldPanel
from django import forms

from .models import AiLabUseCase


class AiLabUseCaseAdmin(ModelAdmin):
    model = AiLabUseCase
    menu_label = "Ai Lab Use Cases"
    menu_icon = "cog"
    add_to_settings_menu = True

    panels = [
        FieldPanel("name"),
        FieldPanel("description", widget=forms.Textarea),
    ]


modeladmin_register(AiLabUseCaseAdmin)
