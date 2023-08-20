import time
import enum
import asyncio
import inspect
from pydantic import BaseModel
from structlog import get_logger
from ._utils import callable_name

log = get_logger()


class RateLimit:
    """
    Limit the rate of flow based on the last call time.
    """

    def __init__(self, edge_func, requests_per_second=1):
        self.edge_func = edge_func
        self.requests_per_second = requests_per_second
        self.last_call = None

    def __repr__(self):
        return f"RateLimit({callable_name(self.edge_func)}, {self.requests_per_second})"

    async def __call__(self, item: BaseModel) -> BaseModel:
        if self.last_call is None:
            self.last_call = time.time()
        else:
            diff = (1 / self.requests_per_second) - (time.time() - self.last_call)
            if diff > 0:
                log.debug("RateLimit sleep", seconds=diff, last_call=self.last_call)
                await asyncio.sleep(diff)
        self.last_call = time.time()
        result = self.edge_func(item)
        if inspect.isawaitable(result):
            return await result
        return result


class Retry:
    """
    Retry an edge a number of times.
    """

    def __init__(self, edge_func, retries=1):
        self.edge_func = edge_func
        self.retries = retries

    def __repr__(self):
        return f"Retry({callable_name(self.edge_func)}, {self.retries})"

    async def __call__(self, item: BaseModel) -> BaseModel:
        exception = None
        for n in range(self.retries + 1):
            try:
                return await self.edge_func(item)
            except Exception as e:
                exception = e
                log.error(
                    "Retry", exception=str(e), retry=n + 1, max_retries=self.retries
                )
        # if we get here, we've exhausted our retries
        # (conditional appeases mypy)
        if exception:
            raise exception


class IfFalse(enum.Enum):
    drop = "drop"
    send = "send"


class Conditional:
    """
    Only call the edge if the condition is true.
    """

    def __init__(self, edge_func, condition, if_false=IfFalse.drop):
        self.edge_func = edge_func
        self.condition = condition
        self.if_false = if_false
        if if_false not in IfFalse:
            raise ValueError(f"if_false must be one of {IfFalse}")

    def __repr__(self):
        return f"Conditional({callable_name(self.edge_func)}, {callable_name(self.condition)})"

    async def __call__(self, item: BaseModel) -> BaseModel:
        result = self.condition(item)
        lg = log.bind(conditional=self, result=result)
        if self.condition(item):
            lg.info("conditional", edge_func=callable_name(self.edge_func))
            result = self.edge_func(item)
            if inspect.isawaitable(result):
                return await result
            return result
        elif self.if_false == IfFalse.drop:
            lg.debug("conditional", if_false=self.if_false)
            return
        elif self.if_false == IfFalse.send:
            lg.debug("conditional", if_false=self.if_false)
            return item
