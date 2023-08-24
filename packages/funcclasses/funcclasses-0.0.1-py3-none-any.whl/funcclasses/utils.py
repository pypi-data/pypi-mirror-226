from typing import Callable, ParamSpec, TypeVar, cast

P = ParamSpec("P")
T = TypeVar("T")


class BoundCache:
    data: dict[str, any]

    def __init__(self) -> None:
        self.data = {}

    def cache(self, func: Callable[P, T]) -> Callable[P,T]:
        name = func.__qualname__
        def cached(*args: P.args, **kwargs: P.kwargs) -> T:
            data = self.data.get(name)
            if data is None:
                data = func(*args, **kwargs)
                self.data[name] = data
            return data
        return cached
