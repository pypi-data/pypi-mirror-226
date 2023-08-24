from lobsang.answers.base import Answer


class TextAnswer(Answer):
    """
    The text answer. Use if you don't need any special formatting.
    This is the default answer in lobsang. Use it if you want a plain text response from the LLM.

    :ivar instructions: The instructions to be used to generate the answer.
    """
    instructions = "{message}"

    def __init__(self, instructions: str = None):
        """
        Initializes the TextAnswer.

        :param instructions: Instructions to override the default instructions (optional).
        """
        super().__init__(instructions=self.instructions)

    def parse(self, response: str, **kwargs) -> None:
        """
        No parsing is required for the text answer.

        :param response: The response from the LLM. This is ignored.
        :return: None (always). No parsing is required for the text answer, so no parsed data is returned.
        """
        return None
