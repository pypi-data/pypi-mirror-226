# -*- coding: utf-8 -*-
"""
validator interface module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject


class AbstractValidatorBase(CoreObject):
    """
    abstract validator base class.

    all application validators must be subclassed from this.
    """

    @abstractmethod
    def validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        it returns the same or fixed value.

        :param object | list[object] value: value to be validated.

        :keyword bool for_update: specifies that this field is being
                                  validated for update operation.
                                  defaults to False if not provided.

        :keyword bool for_find: specifies that validation is for find operation.
                                defaults to False if not provided.
                                if this validator is for find and `for_find=False`
                                is provided, no validation will be done.

        :keyword str field_name: a custom field name to be used in validation errors.

        :keyword bool ignore_default: do not consider default value of the column
                                      for nullability validation. defaults to False
                                      if not provided and if the value is None but
                                      the column has default value it will be
                                      considered as valid.

        :raises CoreNotImplementedError: core not implemented error.
        :raises ValidationError: validation error.

        :returns: object | list[object]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_info(self, for_update=False):
        """
        gets the info of this validator.

        :param bool for_update: specifies that info must be for update operation.
                                defaults to False if not provided and the info of
                                create will be returned.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: dict(bool required: is required for specified operation,
                       str form_field_type: form field type)

        :rtype: dict
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def name(self):
        """
        gets the name of this validator.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def domain(self):
        """
        gets the domain of this validator.

        domain is the type of a BaseEntity subclass that
        this validator validates a value of it.
        if a validator is not specific to an entity, then
        domain could be a unique string name.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type[BaseEntity] | str
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def for_find(self):
        """
        gets a value indicating that this validator should only be used on validation for find.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
