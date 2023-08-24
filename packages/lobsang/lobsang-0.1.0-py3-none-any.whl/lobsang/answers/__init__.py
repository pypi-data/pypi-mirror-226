"""
This package contains the different types of answers that Lobsang can generate.

Note that an answer has two parts: the directive and the parser.
The directive embeds instructions for the LLM to follow and the parser parses the response from the LLM.

For example, a JSONAnswer will embed specific instructions for the LLM to follow and to return a JSON response.
Since, the LLM only returns text, the JSONDirective will try to parse the response as JSON and return the result.
If the response is not valid JSON, a ParseError will be raised with details about the error.
"""

from lobsang.answers.base import Answer
from lobsang.answers.text import TextAnswer
from lobsang.answers.json import JSONAnswer
