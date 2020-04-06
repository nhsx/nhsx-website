from helpers.service import Service

from modules.images.models import NHSXImage


class NHSXImageService(Service):
    __model__ = NHSXImage


_images = NHSXImageService()
