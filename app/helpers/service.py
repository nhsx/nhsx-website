# -*- coding: utf-8 -*-

"""
    helpers.service
    ~~~~~~~~~~~~~~~
    Core Service class
"""
from typing import Optional
from django.http import Http404
from django.db import models


class Service(object):
    """Core service class for abstracting business logic from our models.

    Extend this service to make custom services for models. Keep logic in the
    service, state in the model. Try to never create a model directly, only through
    its service.
    """

    __model__: Optional[models.Model] = None

    def __init__(self, *args, **kwargs):
        self.manager = self.__model__.objects
        super().__init__(*args, **kwargs)

    @property
    def q(self) -> models.query.QuerySet:
        """Base query set used by all the other service methods.
        Override this if you need your service to only return from a subset,
        ie: if you have soft deletes, you can pre-filter on deleted=False

        Returns:
            QuerySet: The qs for this service
        """
        if self.__model__ is None:
            raise ValueError("Missing model for this service")

        return self.__model__.objects

    def count(self) -> int:
        """Override count to operate on the base q

        Returns:
            int: The count
        """
        # logger.info('SERVICE COUNT')
        return self.q.count()

    def _isinstance(self, model: models.Model, raise_error: bool = True) -> bool:
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        Args:
            model (models.Model): the model instance to check
            raise_error (bool, optional): flag to raise an error on a mismatch

        Returns:
            bool: If the model instance matches or not

        Raises:
            ValueError: Raised if there's a mismatch
        """
        if self.__model__ is None:
            raise ValueError("Missing model for this service")

        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError("%s is not of type %s" % (model, self.__model__))
        return rv

    def save(self, model: models.Model) -> models.Model:
        """Commits the model to the database and returns the model

        Args:
            model (models.Model): the model to save

        Returns:
            models.Model: The saved instance
        """
        self._isinstance(model)
        model.save()
        return model

    def all(self) -> models.query.QuerySet:
        """Returns a generator containing all instances of the service's model.

        Returns:
            models.query.QuerySet: All instances.
        """
        return self.q.all()

    def get(self, id: int) -> models.Model:
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        Args:
            id (int): the instance id

        Returns:
            models.Model: An instance if found
        """
        return self.q.get(id=id)

    def find(self, **kwargs) -> models.query.QuerySet:
        """Returns a query set of instances of the service's model filtered by the
        specified key word arguments.

        Args:
            **kwargs: filter parameters

        Returns:
            models.query.QuerySet: A qs filtered by the kwargs
        """
        return self.q.filter(**kwargs)

    def first_or_404(self, **kwargs) -> models.Model:
        """Returns the first instance of the service's model filtered by the
        specified key word arguments.

        Args:
            **kwargs: filter parameters

        Raises:
            Http404: A 404 if nothing is found
        """
        if self.__model__ is None:
            raise ValueError("Missing model for this service")

        try:
            return self.q.get(**kwargs)
        except self.__model__.DoesNotExist:
            raise Http404("Nothing found")

    def first(self, **kwargs) -> models.Model:
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.


        Args:
            **kwargs: filter parameters

        Returns:
            models.Model: The first model found matching the filters

        """
        return self.find(**kwargs).first()

    def last(self, **kwargs) -> models.Model:
        """Returns the last instance found of the service's model filtered by
        the specified key word arguments.

        Args:
            **kwargs: filter parameters

        Returns:
            models.Model: The last saved model matching the filters

        """
        try:
            return self.q.order_by("created_at").reverse().all()[0]
        except Exception:
            try:
                return self.q.reverse().all()[0]
            except Exception:
                return None

    def get_or_404(self, id: int) -> models.Model:
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        Args:
            id (int): the instance id

        Returns:
            models.Model: The model found

        Raises:
            Http404: If no model is found
        """
        if self.__model__ is None:
            raise ValueError("Missing model for this service")
        try:
            return self.q.get(id=id)
        except self.__model__.DoesNotExist:
            raise Http404("Nothing found")

    def get_or_create(self, **kwargs) -> models.Model:
        """Finds an instance if it exactly matches kwargs, otherwise creates a new one.

        Args:
            **kwargs: The properties of the model we're creating

        Returns:
            models.Model: A found or created model
        """
        found = self.first(**kwargs)
        if found is None:
            return self.create(**kwargs)
        else:
            return found

    def new(self, **kwargs) -> models.Model:
        """Returns a new, unsaved instance of the service's model class.

        Args:
            **kwargs: instance parameters

        Returns:
            models.Model: A new, unsaved instance
        """
        if self.__model__ is None:
            raise ValueError("Missing model for this service")

        return self.__model__(**kwargs)

    def create(self, **kwargs) -> models.Model:
        """Returns a new, saved instance of the service's model class.

        Args:
            **kwargs: instance parameters

        Returns:
            models.Model: Our new, saved instance
        """
        return self.save(self.new(**kwargs))

    def update(self, model: models.Model, **kwargs) -> models.Model:
        """Returns an updated instance of the service's model class.

        Args:
            model (models.Model): the model to update
            **kwargs: update parameters

        Returns:
            models.Model: Our updated, saved instance
        """
        self._isinstance(model)
        for k, v in list(kwargs.items()):
            setattr(model, k, v)
        self.save(model)
        return model

    def prepare(self, model: models.Model, **kwargs) -> models.Model:
        """Like update, but doesn't save the model. Use this when you know
        you're going to do something else to it before saving.

        Args:
            model (models.Model): the model to update
            **kwargs: update parameters

        Returns:
            models.Model: The updated but unsaved instance
        """
        self._isinstance(model)
        for k, v in list(kwargs.items()):
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model: models.Model) -> None:
        """Immediately deletes the specified model instance.

        Args:
            model (models.Model): the model instance to delete
        """
        self._isinstance(model)
        model.delete()
