from abc import abstractmethod
from functools import partial

from typing import Callable, TypeVar, Generic, Union, Optional

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")
TError = TypeVar("TError")
TFold = TypeVar("TFold")


# from OSlash library, copied it to avoid external dependencies and issues especially for migration to python 11


class Either(Generic[TSource, TError]):
    """The Either Monad.

    Represents either a successful computation, or a computation that
    has failed.
    """

    @abstractmethod
    def map(self, _: Callable[[TSource], TResult]) -> "Either[TResult, TError]":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def pure(
        cls, value: Callable[[TSource], TResult]
    ) -> "Either[Callable[[TSource], TResult], TError]":
        raise NotImplementedError

    @abstractmethod
    def apply(
        self: "Either[Callable[[TSource], TResult], TError]",
        something: "Either[TSource, TError]",
    ) -> "Either[TResult, TError]":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def unit(cls, value: TSource) -> "Right[TSource, TError]":
        raise NotImplementedError

    @abstractmethod
    def bind(
        self, func: Callable[[TSource], "Either[TResult, TError]"]
    ) -> "Either[TResult, TError]":
        raise NotImplementedError

    @abstractmethod
    def fold(
        self, right: Callable[[TSource], TFold], left: Callable[[TError], TFold]
    ) -> TFold:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other) -> bool:
        raise NotImplementedError

    def __or__(self, func):
        return self.bind(func)

    def is_left(self) -> bool:
        pass

    def is_right(self) -> bool:
        pass


class Right(Either[TSource, TError]):
    """Represents a successful computation."""

    def __init__(self, value: TSource) -> None:
        self._value = value

    # Functor Section
    # ===============

    def map(self, mapper: Callable[[TSource], TResult]) -> Either[TResult, TError]:
        result = mapper(self._value)
        return Right(result)

    # Applicative Section
    # ===================

    @classmethod
    def pure(
        cls, value: Callable[[TSource], TResult]
    ) -> "Right[Callable[[TSource], TResult], TError]":
        return Right(value)

    def apply(
        self: "Right[Callable[[TSource], TResult], TError]",
        something: "Either[TSource, TError]",
    ) -> "Either[TResult, TError]":
        def mapper(other_value):
            try:
                return self._value(other_value)
            except TypeError:
                return partial(self._value, other_value)

        return something.map(mapper)

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: TSource) -> "Right[TSource, TError]":
        return Right(value)

    def bind(
        self, func: Callable[[TSource], Either[TResult, TError]]
    ) -> Either[TResult, TError]:
        return func(self._value)

    def fold(
        self, right: Callable[[TSource], TFold], left: Callable[[TError], TFold]
    ) -> TFold:
        return right(self._value)

    # Operator Overloads
    # ==================

    def __eq__(self, other) -> bool:
        return isinstance(other, Right) and self._value == other._value

    def __str__(self) -> str:
        return "Right %s" % self._value

    @property
    def value(self):
        return self._value

    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True


class Left(Either[TSource, TError]):
    """Represents a computation that has failed."""

    def __init__(self, error: TError) -> None:
        self._error = error

    @property
    def error(self):
        return self._error

    @classmethod
    def pure(
        cls, value: Callable[[TSource], TResult]
    ) -> Either[Callable[[TSource], TResult], TError]:
        return Right(value)

    def apply(self, something: Either) -> Either:
        return Left(self._error)

    def map(self, mapper: Callable[[TSource], TResult]) -> Either[TResult, TError]:
        return Left(self._error)

    @classmethod
    def unit(cls, value: TSource):
        return Right(value)

    def bind(
        self, func: Callable[[TSource], Either[TResult, TError]]
    ) -> Either[TResult, TError]:
        return Left(self._error)

    def fold(
        self, right: Callable[[TSource], TFold], left: Callable[[TError], TFold]
    ) -> TFold:
        return left(self._error)

    def __eq__(self, other) -> bool:
        return isinstance(other, Left) and self._error == other._error

    def __str__(self) -> str:
        return "Left: %s" % self._error

    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False


T = TypeVar("T")


def value_or_raise(either: Either[T, Exception]) -> T:
    value_or_error: Union[T, Exception] = either.fold(lambda x: x, lambda y: y)
    if isinstance(value_or_error, Exception):
        raise value_or_error
    else:
        return value_or_error
