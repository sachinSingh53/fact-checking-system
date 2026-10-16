from typing import Any, Protocol, TypeVar

from pydantic import BaseModel

StructuredResult = TypeVar("StructuredResult", bound=BaseModel)


class StructuredLLMProvider(Protocol):
    """Boundary for schema-constrained model output.

    Concrete providers and domain prompts are introduced only by an approved spec.
    """

    async def generate(
        self,
        *,
        instructions: str,
        input_text: str,
        response_model: type[StructuredResult],
        metadata: dict[str, Any] | None = None,
    ) -> StructuredResult: ...
