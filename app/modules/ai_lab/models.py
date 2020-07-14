from modules.core.models.pages import SectionPage
from django.db import models

class AiLabHomePage(SectionPage):
  max_count = 1

class AiLabUseCase(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255)

  def __str__(self):
    return self.name
