import gevent
from gevent import monkey

from . import LazyList

monkey.patch_all()

from .abstractlist import AbstractList
from typing import List, TypeVar, Callable, Iterable

T = TypeVar("T")
U = TypeVar("U")


class GreenParList(AbstractList[T]):
	"""
	A GreenParList class that behaves like a list and a generator.
	The elements are processed in parallel using green threads.
	"""

	def __init__(self, iterable: Iterable[T]) -> None:
		"""Initializes a GreenParList."""
		super().__init__(iterable)

	def map(self, func: Callable[[T], U]) -> 'GreenParList[U]':
		"""Transforms the elements using the given function with green threads."""
		greenlets = [gevent.spawn(func, item) for item in self]
		gevent.joinall(greenlets)
		results = [greenlet.value for greenlet in greenlets]

		return GreenParList(results)

	def flatmap(self, func: Callable[[T], List[U]]) -> 'GreenParList[U]':
		"""Transforms the elements using the given function, flattening the result."""
		greenlets = [gevent.spawn(func, item) for item in self]
		gevent.joinall(greenlets)
		results = [item for greenlet in greenlets for item in greenlet.value]
		return GreenParList(results)

	def filter(self, predicate: Callable[[T], bool]) -> 'GreenParList[T]':
		"""Filters the elements based on the given predicate."""
		greenlets = [gevent.spawn(lambda x: x if predicate(x) else None, item) for item in self]
		gevent.joinall(greenlets)
		results = [greenlet.value for greenlet in greenlets if greenlet.value is not None]
		return GreenParList(results)

	def fold_left(self, initial: U, func: Callable[[U, T], U]) -> U:
		"""Folds the elements from left to right using the given function and initial value."""

		# Divide the list into chunks
		chunk_size = max(1, len(self) // gevent.getcurrent().minimal_ident)
		chunks = [self[i:i + chunk_size] for i in range(0, len(self), chunk_size)]

		# Conquer: Fold each chunk sequentially
		def fold_chunk(chunk):
			result = initial
			for item in chunk:
				result = func(result, item)
			return result

		greenlets = [gevent.spawn(fold_chunk, chunk) for chunk in chunks]
		gevent.joinall(greenlets)

		# Combine the results of the chunks
		results = [greenlet.value for greenlet in greenlets]
		final_result = initial
		for result in results:
			final_result = func(final_result, result)

		return final_result

	def reduce(self, func: Callable[[T, T], T]) -> T:
		"""Reduces the elements using the given function."""

		if not self:
			raise ValueError("Reduce on empty list")

		# Divide the list into chunks
		chunk_size = max(1, len(self) // gevent.getcurrent().minimal_ident)
		chunks = [self[i:i + chunk_size] for i in range(0, len(self), chunk_size)]

		# Conquer: Reduce each chunk sequentially
		def reduce_chunk(chunk):
			result = chunk[0]
			for item in chunk[1:]:
				result = func(result, item)
			return result

		greenlets = [gevent.spawn(reduce_chunk, chunk) for chunk in chunks]
		gevent.joinall(greenlets)

		# Combine the results of the chunks
		results = [greenlet.value for greenlet in greenlets]
		final_result = results[0]
		for result in results[1:]:
			final_result = func(final_result, result)

		return final_result

	def append(self, item: T) -> "GreenParList[T]":
		"""Appends the given item to the end of the list."""
		self.insert(len(self), item)
		return self

	def extend(self, iterable: List[T]) -> "GreenParList[T]":
		"""Extends the list with the given iterable."""
		for item in iterable:
			self.append(item)
		return self

	def insert(self, index: int, item: T) -> "GreenParList[T]":
		"""Inserts the given item at the specified index."""
		self[index:index] = [item]
		return self

	def pop(self, index: int = -1) -> T:
		"""Removes and returns the item at the specified index (default is the last item)."""
		item = self[index]
		del self[index]
		return item

	def prepend(self, item: T) -> "GreenParList[T]":
		"""Prepends the given item to the beginning of the list."""
		self.insert(0, item)
		return self

	def remove(self, item: T) -> "GreenParList[T]":
		"""Removes the first occurrence of the given item from the list."""
		index = self.index(item)
		del self[index]
		return self
