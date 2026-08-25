import ast
import inspect
import re
from typing import Any


class DefaultExtractor:
    """Extracts source-code representations of default_factory callables."""

    def extract_default_factory(self, default_factory: Any) -> str:
        if default_factory in (list, dict, set, tuple, frozenset):
            return default_factory.__name__
        try:
            source = inspect.getsource(default_factory)
            match = re.search(r"lambda:\s*.*?(?=\s*[,)])", source, re.DOTALL)
            if match:
                lambda_code = match.group(0).strip()
                try:
                    ast.parse(lambda_code, mode="eval")
                    return lambda_code
                except SyntaxError:
                    pass
            return f"lambda: {repr(default_factory())}"
        except (OSError, TypeError, AttributeError):
            return f"lambda: {repr(default_factory())}"
