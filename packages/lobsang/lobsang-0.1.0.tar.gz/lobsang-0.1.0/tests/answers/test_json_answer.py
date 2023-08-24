import textwrap

import pytest

from lobsang.answers.base import ParseError
from lobsang.answers.json import JSONAnswer, DEFAULT_INSTRUCTIONS


@pytest.fixture
def json_answer():
    """
    Return a JSONAnswer instance
    """

    schema = {
        'type': 'object',
        'title': 'Test',
        'required': ['test'],
        'properties': {
            'test': {
                'type': 'string',
                'description': 'The test string.'
            }
        }
    }
    example = {
        'test': 'Hello, world'
    }

    return JSONAnswer(schema=schema, example=example)


def test_inheritance(json_answer):
    """
    Test inheritance of JSONAnswer.
    """
    assert isinstance(json_answer, JSONAnswer)
    assert hasattr(json_answer, "instructions")
    assert json_answer.instructions == DEFAULT_INSTRUCTIONS


def test_directive(json_answer):
    """
    Test the directive method of JSONAnswer.
    """
    message = "Hello, world!"
    directive = json_answer.directive(message)

    schema = json_answer.schema
    example = json_answer.example
    assert directive == textwrap.dedent(
        json_answer.instructions.format(message=message, schema=schema, example=example))


def test_parse(json_answer):
    """
    Test the parse method of JSONAnswer.
    """
    response = """
        This is some text around the JSON block.
        ```json
        {
            "test": "This is a test"
        }
        ```
        This is some text after the JSON block.
        """
    parsed = json_answer.parse(response)
    assert parsed == {'test': 'This is a test'}


def test_no_json_block(json_answer):
    """
    Test the parse method with a response without a JSON block.
    """
    response = "This is some text without a JSON block."

    try:
        json_answer.parse(response)
    except ParseError as e:
        assert e.args[0] == 'No JSON block found.'


def test_invalid_json(json_answer):
    """
    Test the parse method with invalid JSON.
    """
    response = """
    This is some text around the JSON block.
    ```json
    {
        # Here is the error
        'test2': "Hello, world"
    }
    ```

    This is some text after the JSON block.
    """
    try:
        json_answer.parse(response)
    except ParseError as e:
        assert e.args[0].startswith('Invalid JSON. Decode Error:')


def test_schema_mismatch(json_answer):
    """
    Test the parse method with a response that does not match the schema.
    """
    response = """
    This is some text around the JSON block.
    ```json
    {
        "test1": 123
    }
    ```
    This is some text after the JSON block.
    """
    try:
        json_answer.parse(response)
    except ParseError as e:
        assert e.args[0].startswith('Does not match schema. Validation Error:')