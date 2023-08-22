from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Callable
from attr import define, field, Factory
from griptape.core import ExponentialBackoffMixin, PromptStack
from griptape.tokenizers import BaseTokenizer

if TYPE_CHECKING:
    from griptape.artifacts import TextArtifact
    from griptape.structures import Structure


@define
class BasePromptDriver(ExponentialBackoffMixin, ABC):
    temperature: float = field(default=0.1, kw_only=True)
    max_tokens: Optional[int] = field(default=None, kw_only=True)
    structure: Optional[Structure] = field(default=None, kw_only=True)
    prompt_stack_to_string: Callable[[PromptStack], str] = field(
        default=Factory(
            lambda self: self.default_prompt_stack_to_string_converter,
            takes_self=True
        ),
        kw_only=True
    )

    model: str
    tokenizer: BaseTokenizer

    def max_output_tokens(self, text: str) -> int:
        if self.max_tokens:
            return self.max_tokens
        else:
            return self.tokenizer.tokens_left(text)

    def run(self, prompt_stack: PromptStack) -> TextArtifact:
        for attempt in self.retrying():
            with attempt:
                result = self.try_run(prompt_stack)

                return result

    def default_prompt_stack_to_string_converter(self, prompt_stack: PromptStack) -> str:
        prompt_lines = []

        for i in prompt_stack.inputs:
            if i.is_user():
                prompt_lines.append(f"User: {i.content}")
            elif i.is_assistant():
                prompt_lines.append(f"Assistant: {i.content}")
            else:
                prompt_lines.append(i.content)

        return "\n\n".join(prompt_lines)

    @abstractmethod
    def try_run(self, prompt_stack: PromptStack) -> TextArtifact:
        ...
