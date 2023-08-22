from pydantic import Field
from typing import List, Optional, Union, Any, Dict

from promptulate.tools.base import BaseTool
from promptulate.tools.python_repl.api_wrapper import PythonREPLAPIWrapper


class PythonREPLTool(BaseTool):
    """A tool for running python code in a REPL."""

    name: str = "Python_REPL"
    description: str = (
        "A Python shell. Use this to execute python commands. "
        "Input should be a valid python command. "
        "If you want to see the output of a value, you should print it out "
        "with print(...)."
    )
    few_show_example: List[str] = [
        "```python\nage = 25\nresult = age ** 0.43\nprint(result)\n```",
    ]

    api_wrapper: PythonREPLAPIWrapper = Field(default_factory=PythonREPLAPIWrapper)

    def _run(self, command: str, *args, **kwargs) -> str:
        return self.api_wrapper.run(command)
