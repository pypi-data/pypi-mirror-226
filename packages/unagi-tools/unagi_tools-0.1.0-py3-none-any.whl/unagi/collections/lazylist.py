from types import TracebackType
from typing import Iterable, Union, Callable, Any, Iterator, List, TypeVar, Generator, Type, Optional

from .abstractlist import AbstractList

T = TypeVar("T")
U = TypeVar("U")


class LazyList(AbstractList[T], Generator[T, None, None]):
	"""
	A LazyList class that behaves like a list and a generator.

	Can be initialized with an iterable, generator function, or generator object.
	Evaluates elements lazily and caches the results for repeated access.

	Example usage:
		lazy_list = LazyList(range(10))
		result = lazy_list.map(lambda x: x * 2).filter(lambda x: x > 5)

	Attributes:
		cache (List[T]): A list of evaluated elements.
		generator (Union[Iterator[T], Any]): An iterator over the elements.
		generator_func (Callable[[], Iterator[T]]): A function that returns an iterator over the elements.
	"""

	cache: List[T]
	generator: Union[Iterator[T], Any]
	generator_func: Callable[[], Iterator[T]]

	def __init__(self, iterator: Union[Iterable[T], Callable[[], Iterator[T]], Generator[T, None, None]] = None) -> None:
		"""Initialize a LazyList from an iterable, generator function, or generator object."""
		if callable(iterator):
			self.generator_func = iterator
		elif isinstance(iterator, Generator):
			self.generator_func = lambda: iterator  # Use the generator object directly
		elif iterator is None:
			self.generator_func = lambda: iter([])  # Empty generator
		else:
			self.generator_func = lambda: (item for item in iterator)  # Wrap in a lambda function

		self.generator = iter(self.generator_func())  # Create the generator
		self.cache = []
		super().__init__(self)

	def __getitem__(self, index: int) -> T:
		"""Get the item at the given index, evaluating as needed."""
		while len(self.cache) <= index:
			self.cache.append(next(self.generator))
		return self.cache[index]

	def __iter__(self) -> Iterator[T]:
		"""Iterate over the elements, evaluating them lazily."""
		for item in self.cache:
			yield item
		for item in self.generator:
			self.cache.append(item)
			yield item

	def send(self, value: None) -> T:
		"""
		Send a value into the generator (ignored in this implementation).
		Delegates to the next function to continue iterating.
		"""
		return next(self)

	def throw(self, typ: Type[BaseException], val: Optional[Any] = None, tb: Optional[TracebackType] = None) -> T:
		"""
		Raise an exception inside the generator.
		Since LazyList is not designed to handle exceptions in this way,
		it raises a StopIteration exception to signal that the generator is done.
		"""
		raise StopIteration

	def close(self) -> None:
		"""
		Close the generator and free any associated resources.
		Since LazyList doesn't manage any resources that need explicit closing,
		this method provides an empty implementation.
		"""
		pass

	def map(self, func: Callable[[T], U]) -> 'LazyList[U]':
		"""Transform each element using the given function."""
		return LazyList(lambda: (func(x) for x in self))

	def flatmap(self, func: Callable[[T], Iterable[U]]) -> 'LazyList[U]':
		"""Apply a function to each element and flatten the result."""
		return LazyList(lambda: (y for x in self for y in func(x)))

	def filter(self, predicate: Callable[[T], bool]) -> 'LazyList[T]':
		"""Filter elements according to the given predicate."""
		return LazyList(lambda: (x for x in self if predicate(x)))

	def fold_left(self, initial: U, func: Callable[[U, T], U]) -> U:
		"""Reduce elements from left to right using the given function and initial value."""
		result = initial
		for item in self:
			result = func(result, item)
		return result

	def reduce(self, func: Callable[[T, T], T]) -> T:
		"""Reduce elements to a single value using the given function."""
		it = iter(self)
		try:
			result = next(it)
		except StopIteration:
			raise TypeError("Reduce of empty sequence with no initial value")
		for item in it:
			result = func(result, item)
		return result

	def append(self, item: T) -> 'LazyList[T]':
		"""Append one item to the list."""

		def new_generator_func():
			yield from self.generator_func()
			yield item

		self.generator_func = new_generator_func
		return self

	def prepend(self, item: T) -> 'LazyList[T]':
		"""Prepend one item to the list."""

		def new_generator_func():
			yield item
			yield from self.generator_func()

		self.generator_func = new_generator_func
		return self

	def extend(self, items: Iterable[T]) -> 'LazyList[T]':
		"""Extend the list by appending all the items from the iterable."""
		for item in items:
			self.append(item)
		return self

	def insert(self, index: int, item: T) -> "LazyList[T]":
		"""Insert an item at the specified index."""
		while len(self.cache) <= index:
			self.cache.append(next(self.generator))
		self.cache.insert(index, item)
		return self

	def remove(self, item: T) -> "LazyList[T]":
		"""Remove the first occurrence of the item from the list."""
		self.cache.remove(item)
		return self

	def pop(self, index: int = -1) -> T:
		"""Remove and return the item at the specified index (default is the last item)."""
		while len(self.cache) <= index:
			self.cache.append(next(self.generator))
		return self.cache.pop(index)

	def reverse(self) -> 'AbstractList[T]':
		"""Return a reversed version of the list."""
		return LazyList(reversed(self))
