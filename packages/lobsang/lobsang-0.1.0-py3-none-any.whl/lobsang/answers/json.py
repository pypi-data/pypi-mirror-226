import json
import re

import jsonschema
from jsonschema.validators import validator_for, validate

from lobsang.answers.base import Answer, ParseError

DEFAULT_INSTRUCTIONS = """\
{message}

Create a JSON object with the following schema:
```json
{schema}
```

Example Response:
```json
{example}
```"""


class JSONAnswer(Answer):
    """
    Answer in the form of a JSON object.

    Lobsang will instruct the LLM to produce a JSON object with the provided schema.
    This might not always work, as the LLM may produce invalid JSON.
    """

    def __init__(self, schema: dict, example: dict = None, instructions: str = DEFAULT_INSTRUCTIONS):
        """
        Initializes the JSONAnswer with the provided schema.

        **Note:** Replacing the original response helps to keep a clean chat history, hinting that
         i.e. any
        text around the JSON from the original response will be removed.

        :param schema: The schema used to parse the data. It should be a valid JSON schema.
        :param example: An example of the JSON object that should be produced (optional).
        :param instructions: Instructions to override the default instructions (optional).
        """
        assert isinstance(schema, dict), "Schema must be a dict."
        assert isinstance(instructions, str), "Instructions must be a string."

        # Check if instructions format is valid
        try:
            instructions.format(message="test", schema="test", example="test")
        except KeyError as e:
            raise ValueError(f"Invalid instructions format. Missing key {e}")

        # Validate schema
        try:
            validator = validator_for(schema)
            validator.check_schema(schema)
        except jsonschema.exceptions.SchemaError as e:
            raise ValueError(f"Invalid schema. Schema Error: {e}")

        # Validate example
        try:
            validate(instance=example, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Invalid example. Validation Error: {e}")

        # Initialize
        super().__init__(instructions=instructions)
        self.schema = schema
        self.example = example
        self.validator = validator

    def directive(self, message: str, **kwargs) -> str:
        """
        Produce a directive (i.e. message + schema + example + instructions) for the LLM.

        :param message: The message to embed in the instructions.
        :param kwargs: Additional arguments to be used in the instructions.
        :return: The directive for the LLM.
        """
        return super().directive(message, schema=self.schema, example=self.example, **kwargs)

    @staticmethod
    def extract(message: str):
        """
        Try to extract content of a JSON block from a message.

        :param message: The message to extract the JSON block from.
        :return: The content of the JSON block or None if no JSON block was found.
        """
        pattern = r'```json\s*(.*?)\s*```'
        match = re.search(pattern=pattern, string=message, flags=re.DOTALL)

        return match.group(1) if match else None

    def parse(self, res: str, **kwargs) -> dict:
        """
        Try to extract and parse a JSON block from a response.

        :param res: The response to parse.
        :return: The (parsed) response
        :raises ParseError: If the response could not be parsed.
        """
        # Try to extract JSON block
        json_block = self.extract(res)

        # Stop early if no JSON block was found
        if not json_block:
            raise ParseError("No JSON block found.")

        # Try to parse JSON block
        try:
            json_object = json.loads(json_block)
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON. Decode Error: {e}")

        # Validate JSON object
        try:
            validate(json_object, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ParseError(f"Does not match schema. Validation Error: {e}")

        # If we get here, the JSON object is valid, so we return it
        return json_object

    @classmethod
    def from_file(cls, path: str, **kwargs):
        """
        Creates a new JSONAnswer from a JSON schema file (without example).

        :param path: The path to the JSON schema file.
        :return: A new instance of the JSONAnswer.
        :raises: FileNotFoundError if the schema file does not exist.
        :raises: jsonschema.exceptions.SchemaError if the schema is invalid.
        """
        with open(path) as schema_file:
            schema = json.load(schema_file)

        return cls(schema=schema, **kwargs)
