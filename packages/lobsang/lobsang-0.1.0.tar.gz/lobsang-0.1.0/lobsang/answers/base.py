import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class ParseError(Exception):
    """
    Represents an error that occurs during parsing.
    """
    pass


@dataclass
class Answer(ABC):
    """
    Abstract class for answer types.

    :ivar instructions: The instructions to be used to generate the answer.
    """
    instructions: str = None

    def directive(self, message: str, **kwargs) -> str:
        """
        Embeds the message in the instructions to generate the expected answer.
        This also dedents the instructions to remove any common indentation.

        Note: Despite creating a directive to instruct the LLM, the response might still be different from the expected
        answer format due to the nature of the LLM (uncertainty, randomness, etc.).

        :param message: The message to embed in the instructions.
        :param kwargs: Additional arguments to be used in the instructions.
        :return: Tuple (str, dict) of the embedded message and an info dict
        """
        dedented = textwrap.dedent(self.instructions)
        formatted = dedented.format(message=message, **kwargs)
        return formatted

    @abstractmethod
    def parse(self, response: str) -> Any:
        """
        Parses the response from the message in the context of the directive.

        :param response: The response to parse.
        :return: The parsed response.
        :raises ParseError: If parsing fails.
        """
        pass
