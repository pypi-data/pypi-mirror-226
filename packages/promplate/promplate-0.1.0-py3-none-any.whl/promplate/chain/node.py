from abc import ABC, abstractclassmethod
from inspect import iscoroutinefunction
from typing import Awaitable, Callable

from promplate.llm.base import *
from promplate.prompt import ChatTemplate, Template
from promplate.prompt.template import Context

Process = Callable[[Context], Context]

AsyncProcess = Callable[[Context], Awaitable[Context]]


class AbstractChain(ABC):
    @abstractclassmethod
    def run(self, context: Context, complete: Complete):
        pass

    @abstractclassmethod
    async def arun(self, context: Context, complete: Complete | AsyncComplete):
        pass


class Node(AbstractChain):
    def __init__(
        self,
        template: Template,
        pre_processes: list[Process | AsyncProcess] | None = None,
        post_processes: list[Process | AsyncProcess] | None = None,
        **config,
    ):
        self.template = template
        self.pre_processes = pre_processes or []
        self.post_processes = post_processes or []
        self.run_config = config

    def run(self, context, complete):
        for process in self.pre_processes:
            context = process(context)

        prompt = self.template.render(context)

        assert isinstance(self.template, ChatTemplate) ^ isinstance(prompt, str)

        result = {"__result__": complete(prompt, **self.run_config)}

        for process in self.post_processes:
            result = process(result)

        return result

    async def arun(self, context, complete):
        for process in self.pre_processes:
            if iscoroutinefunction(process):
                context = await process(context)
            else:
                context = process(context)

        prompt = await self.template.arender(context)

        assert isinstance(self.template, ChatTemplate) ^ isinstance(prompt, str)

        if iscoroutinefunction(complete):
            result = {"__result__": await complete(prompt, **self.run_config)}
        else:
            result = {"__result__": complete(prompt, **self.run_config)}

        for process in self.post_processes:
            if iscoroutinefunction(process):
                context = await process(context)
            else:
                context = process(context)

        return result

    def next(self, chain: AbstractChain):
        if isinstance(chain, Node):
            return Chain(self, chain)
        else:
            return Chain(self, *chain)

    def __add__(self, chain: AbstractChain):
        return self.next(chain)


class Chain(AbstractChain):
    def __init__(self, *nodes: AbstractChain):
        self.nodes = list(nodes)

    def next(self, chain: AbstractChain):
        if isinstance(chain, Node):
            return Chain(*self, chain)
        else:
            return Chain(*self, *chain)

    def __add__(self, chain):
        return self.next(chain)

    def __iter__(self):
        return self.nodes

    def run(self, context, complete):
        for node in self.nodes:
            context = node.run(context, complete)

        return context

    async def arun(self, context, complete):
        for node in self.nodes:
            context = await node.arun(context, complete)

        return context
