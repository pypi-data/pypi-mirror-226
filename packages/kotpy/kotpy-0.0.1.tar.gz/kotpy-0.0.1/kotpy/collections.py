from typing import Callable, Iterable, List, Reversible, TypeVar

T = TypeVar("T")


def take_while_iter(iterable: Iterable[T], predicate: Callable[[T], bool]) -> Iterable[T]:
    """Go through items in an iterable until the predicate function is not True."""
    for item in iterable:
        if predicate(item):
            yield item
        else:
            break


def take_while(iterable: Iterable[T], predicate: Callable[[T], bool]) -> List[T]:
    return list(take_while_iter(iterable, predicate))


def take_last_while(iterable: Reversible[T], predicate: Callable[[T], bool]) -> Iterable[T]:
    """Go through items in an iterable until the predicate function is not True."""
    ret = []
    for item in reversed(iterable):
        if predicate(item):
            ret.insert(0, item)
        else:
            break
    return ret
