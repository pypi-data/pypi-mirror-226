from concurrent.futures import ThreadPoolExecutor
from typing import List, TypeVar, Callable, Iterable

from . import AbstractList

T = TypeVar("T")
U = TypeVar("U")


class ParList(AbstractList[T]):
	def __init__(self, iterable: Iterable[T] = None, thread_pool: ThreadPoolExecutor = None, max_workers=None, thread_name_prefix='',
			initializer=None, initargs=()
	) -> None:
		"""Initializes a ParList with an optional custom thread pool.

		Args:
			iterable (List[T]): The input iterable to be processed.
			thread_pool (ThreadPoolExecutor, optional): A custom thread pool. If None, a new one will be created.
		"""
		super().__init__([] if iterable is None else iterable)
		self.thread_pool = thread_pool if thread_pool else ThreadPoolExecutor(
			max_workers=max_workers,
			thread_name_prefix=thread_name_prefix,
			initializer=initializer,
			initargs=initargs
		)

	def __enter__(self) -> 'ParList':
		"""Returns the ParList itself."""
		return self

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		"""Shuts down the thread pool."""
		self.thread_pool.shutdown()

	def map(self, func: Callable[[T], U]) -> 'ParList[U]':
		"""Transforms the elements using the given function with parallel execution."""
		results = list(self.thread_pool.map(func, self))
		return ParList(results)

	def flatmap(self, func: Callable[[T], List[U]]) -> 'ParList[U]':
		"""Transforms the elements using the given function, flattening the result."""
		results = [item for sublist in self.thread_pool.map(func, self) for item in sublist]
		return ParList(results)

	def filter(self, predicate: Callable[[T], bool]) -> 'ParList[T]':
		"""Filters the elements based on the given predicate."""
		results = [item for item in self if predicate(item)]
		return ParList(results)

	def fold_left(self, initial: U, func: Callable[[U, T], U]) -> U:
		"""Folds the elements from left to right using the given function and initial value."""
		result = initial
		for item in self:
			result = func(result, item)
		return result

	def reduce(self, func: Callable[[T, T], T]) -> T:
		"""Reduces the elements using the given function."""
		if not self:
			raise ValueError("Reduce on empty list")
		result = self[0]
		for item in self[1:]:
			result = func(result, item)
		return result

	def append(self, item: T) -> "ParList[T]":
		"""Appends the given item to the end of the list."""
		self.insert(len(self), item)
		return self

	def extend(self, iterable: Iterable[T]) -> "ParList[T]":
		"""Extends the list by appending all the items from the iterable."""
		for item in iterable:
			self.append(item)
		return self

	def insert(self, index: int, item: T) -> "ParList[T]":
		"""Inserts the given item at the specified index."""
		self[index:index] = [item]
		return self

	def pop(self, index: int = -1) -> T:
		"""Removes and returns the item at the specified index (default is the last item)."""
		item = self[index]
		del self[index]
		return item

	def prepend(self, item: T) -> "ParList[T]":
		"""Prepends the given item to the beginning of the list."""
		self.insert(0, item)
		return self

	def remove(self, item: T) -> "ParList[T]":
		"""Removes the first occurrence of the given item from the list."""
		index = self.index(item)
		del self[index]
		return self
