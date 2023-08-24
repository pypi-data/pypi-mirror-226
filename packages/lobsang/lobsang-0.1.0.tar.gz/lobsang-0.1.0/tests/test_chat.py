import pytest

from lobsang import Chat, UserMessage, AssistantMessage, LLM
from lobsang.answers import Answer, TextAnswer
from lobsang.llms.fake import FakeLLM


class TestAnswer(Answer):
    """
    Dummy directive for testing.
    """
    instructions = "embed {message}"

    def parse(self, response: str, **kwargs) -> (str, dict):
        return f"parse {response}"


class TestLLM(FakeLLM):
    """
    Intercepts messages and stores them in a list.
    """
    messages = None

    def chat(self, messages):
        self.messages = messages
        return super().chat(messages)


@pytest.fixture(scope="function")
def chat():
    chat = Chat([], llm=TestLLM())
    return chat


def test_default(chat):
    """
    Test default behavior.
    """
    assert len(chat.history) == 0, "Expected empty chat."
    assert chat.sys_msg.text == "You are a helpful assistant."
    assert isinstance(chat.llm, LLM)


def test_init_with_messages():
    """
    Test initialization with messages.
    """
    messages = [UserMessage("Hello"), AssistantMessage("Hi")]
    chat = Chat(messages)
    assert chat.history == messages


def test_call(chat):
    """
    Test call method with message chain.
    """
    messages = [UserMessage("Hello"), TextAnswer(), UserMessage("How are you?"), TextAnswer(), UserMessage("Bye"),
                AssistantMessage("Bye")]
    res = chat(messages)

    assert len(res) == 6, "Expected four messages."

    # Check messages one by one
    assert res[0] == messages[0], "Expected first message to be user message."
    assert res[1] == AssistantMessage(text="DUMMY RESPONSE for 'Hello'", info={'directive': 'Hello'}, data=None)
    assert res[2] == messages[2], "Expected third message to be user message."
    assert res[3] == AssistantMessage(text="DUMMY RESPONSE for 'How are you?'", info={'directive': 'How are you?'},
                                      data=None)
    assert res[4] == messages[4], "Expected fifth message to be user message."
    assert res[5] == messages[5], "Expected sixth message to be assistant message."


def test_call_error(chat):
    """
    Test call method with invalid input.
    """
    with pytest.raises(AssertionError):
        chat({})

    with pytest.raises(NotImplementedError):
        chat([1, 2, 3])


def test_call_without_append(chat):
    """
    Test parametrized call method with `append=False`
    """
    assert len(chat.history) == 0, "Expected empty chat."
    chat([UserMessage("Hello")], append=False)
    assert len(chat.history) == 0, "Expected no messages to be added."


def test_invoke(chat):
    """
    Test `chat._invoke(...)` method.
    """
    # Use TestLLM to test if messages are passed down correctly.
    chat.llm = TestLLM()

    # Add message to chat (the context for the test)
    chat.history.append(UserMessage("My name is Bark Twain."))

    # Invoke with TextAnswer as return type
    res = chat._invoke(TextAnswer(), context=chat.history)
    assert isinstance(res, AssistantMessage), "Expected AssistantMessage as return value."
    assert res == AssistantMessage(text="DUMMY RESPONSE for 'My name is Bark Twain.'",
                                   info={'directive': 'My name is Bark Twain.'},
                                   data=None)


def test_copy(chat):
    """
    Test copy method.
    """
    new_chat = chat.copy()
    assert id(new_chat) != id(chat), "Expected new chat instance."
    assert new_chat.llm == chat.llm, "Expected llm to be the same."
    assert new_chat.history == chat.history, "Expected history to be the same."
    assert new_chat.sys_msg == chat.sys_msg, "Expected sys_msg to be the same."
