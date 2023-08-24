import pytest

from lobsang.answers import TextAnswer


@pytest.fixture
def text_answer():
    return TextAnswer()


def test_inheritance(text_answer):
    """
    Test inheritance of TextAnswer.
    """
    assert isinstance(text_answer, TextAnswer)
    assert hasattr(text_answer, "instructions")
    assert text_answer.instructions == "{message}"


def test_directive(text_answer):
    """
    Test the directive method of TextAnswer.
    """
    message = "Hello, world!"
    directive = text_answer.directive(message)
    assert directive == message


def test_parse(text_answer):
    """
    Test the parse method of TextAnswer.
    """
    message = "Hello, world!"
    parsed = text_answer.parse(message)
    assert parsed is None