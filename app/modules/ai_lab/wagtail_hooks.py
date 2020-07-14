from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import AiLabUseCase

class AiLabUseCaseAdmin(ModelAdmin):
    model = AiLabUseCase
    menu_label = "Ai Lab Use Cases"
    menu_icon = "cog"
    add_to_settings_menu = True

modeladmin_register(AiLabUseCaseAdmin)
