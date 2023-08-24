"""
This module contains the core class of Lobsang: the Chat class, which is used to manage a conversation with a LLM.
"""

from lobsang.answers import Answer
from lobsang.llms.base import LLM
from lobsang.messages import Message, SystemMessage, UserMessage, AssistantMessage


class Chat:
    """
    A chat holds a conversation between a user and an assistant and can be called to converse with a LLM.
    """

    def __init__(self, seq: list[Message] = None,
                 sys_msg: SystemMessage = SystemMessage("You are a helpful assistant."),
                 llm: LLM = None) -> None:
        """
        Creates a new chat instance.

        :param seq: A list of messages to initialize the chat history with (see `Chat.history`).
        :param sys_msg: The system message to use for the chat.
        :param llm: The language model to use. Can be set later via `Chat.llm = ...`.
        :raises AssertionError: If parameters are of wrong type.
        """
        seq = seq or []

        assert isinstance(seq, list), f"Expected 'list' but got {type(seq)} for 'seq'."
        assert all(isinstance(m, Message) for m in seq), f"Found non-Message element in 'seq'."
        assert isinstance(sys_msg, SystemMessage), f"Expected 'SystemMessage' but got {type(sys_msg)} for 'sys_msg'."

        # Set attributes
        self.history = list(seq)
        self.sys_msg = sys_msg
        self.llm = llm

    def __call__(self, seq: list[Message | Answer], append: bool = True) -> list[Message]:
        """
        Calls the chat with a seq of messages and answer types, i.e. `chat([user_msg, text_answer, ...])`.
        Returns the conversation with all messages and corresponding responses from the LLM.

        :param seq: The messages and answer types to send to the LLM.
        :param append: Whether to append the conversation to the chat history.
        :return: The conversation with all messages and corresponding responses from the LLM.
        :raises AssertionError: If `seq` is not a sequence.
        :raises ParseError: If the LLM response could not be parsed to the required answer type.
        """
        assert isinstance(seq, list), f"Expected 'list' but got {type(seq)} for 'seq'."

        # Loop through seq and invoke LLM respectively
        conversation = []
        for item in seq:
            if isinstance(item, Message):
                conversation.append(item)
            elif isinstance(item, Answer):
                assistant_message = self._invoke(answer=item, context=[*self.history, *conversation])
                conversation.append(assistant_message)
            else:
                raise NotImplementedError(f"No implementation for {item} of type {type(item)}.")

        # If flag is set, append conversation to chat
        if append:
            self.history.extend(conversation)

        return conversation

    def _invoke(self, answer: Answer, context: list[Message]) -> AssistantMessage:
        """
        Invokes the LLM with the provided answer (type) and context where the LLM generates a response to the last
        message in the context.

        :param answer: The answer (type) to invoke the LLM with.
        :param context: The context to invoke the LLM with (the last message in the context will be used to build the
        query).
        :return: The response from the LLM in form of an assistant message.
        :raises AssertionError: If `context` is empty or contains non-Message elements.
        :raises ParseError: If the LLM response could not be parsed to the required answer type.
        """
        assert len(context) > 0, "Expected non-empty sequence for 'context'."
        assert all(isinstance(m, Message) for m in context), "Expected only elements of type 'Message' in 'context'."

        # Build directive for answer type
        message = context[-1].text
        directive = answer.directive(message)

        # Call LLM with system message, context and the constructed query
        messages = [self.sys_msg, *context[:-1], UserMessage(directive)]
        response, llm_info = self.llm.chat(messages)

        # Parse response
        data = answer.parse(response)

        # Create and return assistant message
        assistant_info = llm_info | {'directive': directive}
        assistant_message = AssistantMessage(text=response, data=data, info=assistant_info)

        return assistant_message

    def copy(self) -> "Chat":
        """
        Returns a shallow copy of the chat instance.

        :return: The shallow copy.
        """
        return Chat(list(self.history), self.sys_msg, self.llm)

    def __str__(self, sep='\n'):
        """
        Returns a string representation of the chat HISTORY.

        :param sep: The separator to use between messages.
        """
        return sep.join(map(str, self.history))

    def __repr__(self):
        """
        Returns a string representation of the chat INSTANCE which can be used to reconstruct the chat instance.
        """
        # Get LLM name
        Chat(self.history, llm=self.llm, sys_msg=self.sys_msg)

        return f"Chat({self.history}, llm={self.llm}, sys_msg={repr(self.sys_msg)})"
