from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable, TypeVar, List, Tuple, Iterable

T = TypeVar("T")
U = TypeVar("U")


class AbstractList(ABC, List[T]):
	def __init__(self, iterable: Iterable[T]) -> None:
		super().__init__(iterable)

	def foreach(self, func: Callable) -> None:
		"""Applies the given function to each item in the list."""
		self.map(func)
		return None

	@abstractmethod
	def map(self, func: Callable[[T], U]) -> 'AbstractList[U]':
		"""Transforms the elements using the given function."""
		pass

	@abstractmethod
	def flatmap(self, func: Callable[[T], List[U]]) -> 'AbstractList[U]':
		"""Transforms the elements using the given function, flattening the result."""
		pass

	@abstractmethod
	def filter(self, predicate: Callable[[T], bool]) -> 'AbstractList[T]':
		"""Filters the elements based on the given predicate."""
		pass

	@abstractmethod
	def fold_left(self, initial: U, func: Callable[[U, T], U]) -> U:
		"""Folds the elements from left to right using the given function and initial value."""
		pass

	@abstractmethod
	def reduce(self, func: Callable[[T, T], T]) -> T:
		"""Reduces the elements to a single value using the given function."""
		pass

	@abstractmethod
	def append(self, items: T) -> "AbstractList[T]":
		"""Append one item to the list."""
		pass

	@abstractmethod
	def prepend(self, items: T) -> "AbstractList[T]":
		"""Prepend one item to the list."""
		pass

	@abstractmethod
	def extend(self, items: Iterable[T]) -> "AbstractList[T]":
		"""Extend the list by appending all the items from the iterable."""
		pass

	@abstractmethod
	def insert(self, index: int, item: T) -> "AbstractList[T]":
		"""Insert an item at the specified index."""
		pass

	@abstractmethod
	def remove(self, item: T) -> "AbstractList[T]":
		"""Remove the first occurrence of the item from the list."""
		pass

	@abstractmethod
	def pop(self, index: int = -1) -> T:
		"""Remove and return the item at the specified index (default is the last item)."""
		pass

	def group_by(self, func: Callable[[T], U]) -> defaultdict[U, List[T]]:
		"""Groups the elements by the key returned by the given function."""
		groups = defaultdict(list)
		for item in self:
			key = func(item)
			groups[key].append(item)
		return groups

	def zip_with_index(self) -> List[Tuple[T, int]]:
		"""Zips the elements with their index."""
		return list(zip(self, range(len(self))))

	def reverse(self) -> 'AbstractList[T]':
		"""Returns a reversed copy of the list."""
		return self.__class__(list(reversed(self)))

	def head_option(self) -> T:
		"""Returns the first element if present, otherwise returns None."""
		return self[0] if self else None

	def head(self) -> T:
		"""Returns the first element, raising an exception if the list is empty."""
		if not self:
			raise IndexError("Head called on an empty list")
		return self[0]

	def tail(self) -> 'AbstractList[T]':
		"""Returns a new list containing all elements except the first one."""
		if not self:
			raise IndexError("Tail called on an empty list")
		return self.__class__(self[1:])
