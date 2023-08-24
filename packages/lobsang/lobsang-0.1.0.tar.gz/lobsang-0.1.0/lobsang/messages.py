"""
This module defines the message classes for the chat module.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any


class Role(StrEnum):
    """
    Represents the role of a message.
    """
    SYSTEM = auto()
    USER = auto()
    ASSISTANT = auto()


@dataclass
class Message(ABC):
    """
    Abstract class for messages.

    :ivar text: The content of the message. Must be non-empty str.
    :ivar info: Additional information about the message.
    :ivar role: The role of the message (Not implemented in the abstract class, see subclasses).
    """
    text: str
    info: dict = field(default_factory=dict)

    @property
    @abstractmethod
    def role(self) -> Role:
        pass

    def __str__(self):
        return f"{self.role.name}: {self.text}"


class SystemMessage(Message):
    """
    Represents a system message.

    :ivar text: The content of the message. Must be non-empty str.
    :ivar info: Additional information about the message.
    :ivar role: The role of the message. Always Role.SYSTEM.
    """
    @property
    def role(self) -> Role:
        return Role.SYSTEM


class UserMessage(Message):
    """
    Represents a user message.

    :ivar text: The content of the message. Must be non-empty str.
    :ivar info: Additional information about the message.
    :ivar role: The role of the message. Always Role.USER.
    """
    @property
    def role(self) -> Role:
        return Role.USER


@dataclass
class AssistantMessage(Message):
    """
    Represents an assistant message.

    :ivar text: The content of the message. Must be non-empty str.
    :ivar data: Parsed data from the message.
    :ivar info: Additional information about the message.
    :ivar role: The role of the message. Always Role.ASSISTANT.
    """
    data: Any = None

    @property
    def role(self) -> Role:
        return Role.ASSISTANT
