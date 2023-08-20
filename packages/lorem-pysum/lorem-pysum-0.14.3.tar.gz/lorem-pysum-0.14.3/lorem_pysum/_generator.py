"""Generate random instances of the given Pydantic model type."""
from __future__ import annotations

__all__ = ("generate",)

import dataclasses
import datetime
import math
import random
import string
import types
import typing
from copy import copy
from enum import Enum
from numbers import Number
from typing import Any, Optional, Type, TypeAlias, TypeVar, Union
from uuid import UUID, uuid4

import annotated_types
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

NoneType = type(None)
ModelType = TypeVar("ModelType", bound=BaseModel)
AnyNumber: TypeAlias = Union[Number, float]
default_max_len = 3
default_date = datetime.date(year=1788, month=6, day=21)
default_time_delta = datetime.timedelta()
default_time = datetime.time()


@dataclasses.dataclass
class Metadata:
    """Filed info metadata."""

    gt: Optional[int] = None
    ge: Optional[int] = None
    lt: Optional[int] = None
    le: Optional[int] = None
    multiple_of: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None


def generate(
    model_type: Type[ModelType],
    use_default_values: bool = True,
    optionals_use_none: bool = False,
    randomize: bool = False,
    overrides: Optional[dict[str, Any]] = None,
) -> ModelType:
    """Generate an instance of a Pydantic model with random values.

    Any values provided in `kwargs` will be used as model field values
    instead of randomly generating them.

    :param model_type: Model type to generate an instance of.
    :param use_default_values: Whether to use model default values.
    :param optionals_use_none: How to handle optional fields.
    :param randomize: Whether to produce randomized values.
    :param overrides: Attributes to manually set on the model instance.
    :return: A randomly generated instance of the provided model type.
    """
    return _Generator(
        model_type,
        use_default_values=use_default_values,
        optionals_use_none=optionals_use_none,
        randomize=randomize,
        overrides=overrides,
    ).generate(model_type)


class _Generator:
    """Class to generate values for a model.

    Use of class here simplifies the function definitions and calls of
    the numerous recursive functions that were previously obligated to
    pass and accept as arguments, the same flags that can be held at a
    class level.
    """

    def __init__(
        self,
        model_type: Type[ModelType],
        *_args,
        use_default_values: bool = True,
        optionals_use_none: bool = False,
        randomize: bool = False,
        overrides: Optional[dict[str, Any]] = None,
    ) -> None:
        self.model_type = model_type
        self.use_default_values = use_default_values
        self.optionals_use_none = optionals_use_none
        self.randomize = randomize
        self.overrides = overrides or {}

    def generate(
        self,
        model_type: Type[ModelType],
        processed_models: Optional[list[Type[ModelType]]] = None,
    ) -> ModelType:
        """Generate an instance of the given model.

        :param model_type: Model type to generate instance of.
        :param processed_models: Models already processed, used for
            recursive calls to prevent infinite recursion.
        :return: Instance of model with fields populated.
        """
        # Copy prevents us from mutating original, if we mutated
        # original, sibling fields could be mistaken as recursive.
        processed_models = copy(processed_models) if processed_models else []
        processed_models.append(model_type)

        for field_name, field_info in model_type.model_fields.items():
            if field_name in self.overrides:
                continue
            _get_metadata(field_info)
            if (
                field_info.default is not PydanticUndefined
                or field_info.default_factory is not None
            ) and self.use_default_values:
                continue

            self.overrides[field_name] = self._get_value(
                field_info.annotation or str, field_info, processed_models
            )
        return model_type(**self.overrides)

    def _get_value(  # noqa: PLR0911,PLR0912
        self,
        type_: Type,
        field_info: FieldInfo,
        processed_models: list[Type[ModelType]],
    ) -> Any:
        metadata = _get_metadata(field_info)
        origin = typing.get_origin(type_)

        if self.optionals_use_none and NoneType in typing.get_args(type_):
            return None

        # If type is dict create dict with proper key and value types.
        if origin is dict:
            k_type, v_type = typing.get_args(type_)
            return {
                self._get_value(k_type, field_info, processed_models): self._get_value(
                    v_type, field_info, processed_models
                )
                for _ in range(default_max_len)
            }

        # If set or list, generate list (Pydantic will coerce list to set).
        if origin in [list, set]:
            return self._get_list_values(type_, field_info, metadata, processed_models)

        # If union, pick among possible types avoiding NoneType.
        if origin and (origin is Union or issubclass(origin, types.UnionType)):
            type_choices = [
                arg_type
                for arg_type in typing.get_args(type_)
                if not issubclass(arg_type, NoneType)
                and arg_type not in processed_models
            ]
            # Only options are `None` or infinite recursion, use `None`.
            if not type_choices:
                return None
            if self.randomize:
                chosen_union_type = random.choice(type_choices)
            else:
                chosen_union_type = type_choices[0]
            return self._get_value(chosen_union_type, field_info, processed_models)

        # Trivial to produce values.
        if type_ == str:
            return self._random_str_value(metadata)
        if type_ in [int, float]:
            return self._random_number_value(metadata)
        if type_ == bool:
            return random.random() > 0.5 if self.randomize else True  # noqa: PLR2004
        if type_ is Any:
            return None
        if type_ == UUID:
            return uuid4()
        if type_ == datetime.date:
            return _random_date_value() if self.randomize else default_date
        if type_ == datetime.time:
            return _random_time_value() if self.randomize else default_time
        if type_ == datetime.timedelta:
            return _random_timedelta_value() if self.randomize else default_time_delta
        if type_ == datetime.datetime:
            return (
                _random_datetime_value()
                if self.randomize
                else datetime.datetime.fromordinal(default_date.toordinal())
            )

        # `issubclass` raises type error on non-classes, these must be
        # done last.
        if issubclass(type_, NoneType):
            return None
        if issubclass(type_, Enum):
            return random.choice(list(type_)) if self.randomize else list(type_)[0]

        # If is child model, add type_ to processed_models and generate child.
        if issubclass(type_, BaseModel):
            return self.generate(type_, processed_models)

        # Catchall.
        return type_()

    def _get_list_values(
        self,
        type_: Type,
        field_info: FieldInfo,
        metadata: Metadata,
        processed_models: list[Type[ModelType]],
    ) -> list[Any]:
        if self.randomize:
            target_length = _get_target_length(metadata.min_length, metadata.max_length)
        else:
            target_length = metadata.min_length or default_max_len

        items: list = []
        list_types = typing.get_args(type_)
        while len(items) < target_length:
            for arg in list_types:
                value = self._get_value(arg, field_info, processed_models)
                items.append(value)
        return items

    def _random_str_value(self, metadata: Metadata) -> str:
        """Get a random string."""
        if self.randomize:
            target_length = _get_target_length(metadata.min_length, metadata.max_length)
            choices = string.ascii_letters + string.digits
            return _random_str(choices, target_length)
        default = "string"
        if (metadata.min_length is None or metadata.min_length <= len(default)) and (
            metadata.max_length is None or metadata.max_length >= len(default)
        ):
            return default
        return "s" * (metadata.min_length or default_max_len)

    def _random_number_value(self, metadata: Metadata) -> AnyNumber:
        """Get a random number."""
        default_max_difference = 256
        iter_size = metadata.multiple_of or 1.0
        # Determine lower bound.
        lower = 0.0
        if ge := metadata.ge:
            while lower < ge:
                lower += iter_size
        if gt := metadata.gt:
            while lower <= gt:
                lower += iter_size
        # Determine upper bound.
        upper = lower + iter_size * default_max_difference
        if le := metadata.le:
            while upper > le:
                upper -= iter_size
        if lt := metadata.lt:
            while upper >= lt:
                upper -= iter_size
        # Re-evaluate lower bound in case ge/gt unset and upper is negative.
        if not metadata.ge and not metadata.gt and lower > upper:
            lower = upper - iter_size * default_max_difference
        # Find an int within determined range.
        if not metadata.multiple_of:
            return random.randint(int(lower), int(upper)) if self.randomize else lower
        if self.randomize:
            max_iter_distance = abs(math.floor((upper - lower) / iter_size))
            return lower + iter_size * random.randint(1, max_iter_distance)
        return lower + iter_size


def _random_datetime_value() -> datetime.datetime:
    dt = datetime.datetime.fromordinal(_random_date_value().toordinal())
    dt += _random_timedelta_value()
    return dt


def _random_date_value() -> datetime.date:
    return datetime.date(
        year=random.randint(1970, 2037),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
    )


def _random_time_value() -> datetime.time:
    return datetime.time(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )


def _random_timedelta_value() -> datetime.timedelta:
    return datetime.timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


def _random_str(choices: str, target_length: int) -> str:
    return "".join(random.choice(choices) for _ in range(target_length))


def _get_target_length(min_length: Optional[int], max_length: Optional[int]) -> int:
    if not min_length:
        if max_length is not None:
            min_length = random.randint(0, max_length - 1)
        else:
            min_length = random.randint(0, default_max_len)
    max_length = max_length or random.randint(1, default_max_len) + min_length
    return random.choice(range(min_length, max_length))


def _get_metadata(field_info: FieldInfo) -> Metadata:
    metadata = Metadata()
    for meta in field_info.metadata:
        if isinstance(meta, annotated_types.Gt):
            metadata.gt = meta.gt  # type: ignore
        elif isinstance(meta, annotated_types.Ge):
            metadata.ge = meta.ge  # type: ignore
        elif isinstance(meta, annotated_types.Lt):
            metadata.lt = meta.lt  # type: ignore
        elif isinstance(meta, annotated_types.Le):
            metadata.le = meta.le  # type: ignore
        elif isinstance(meta, annotated_types.MultipleOf):
            metadata.multiple_of = meta.multiple_of  # type: ignore
        elif isinstance(meta, annotated_types.MinLen):
            metadata.min_length = meta.min_length
        elif isinstance(meta, annotated_types.MaxLen):
            metadata.max_length = meta.max_length
    return metadata
