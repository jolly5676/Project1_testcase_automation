import ast
from backend.base_parser import CodeArtifact

class PythonCodeParser(CodeArtifact):
    """Parses Python code to extract docstrings, functions, and structure."""

    def __init__(self, py_code: str, filename: str):
        super().__init__(py_code, filename)
        self.module_doc = None
        self.functions = []

    def _extract_docstrings_and_functions(self):
        try:
            tree = ast.parse(self.py_code)
        except SyntaxError as e:
            return {"error": f"SyntaxError in {self.filename}: {e}"}

        self.module_doc = ast.get_docstring(tree)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_doc = ast.get_docstring(node)
                func_name = node.name
                func_body = ast.get_source_segment(self.py_code, node)
                self.functions.append({
                    "name": func_name,
                    "doc": func_doc or "",
                    "body": func_body or ""
                })

        return {"module_doc": self.module_doc, "functions": self.functions}

    def process(self):
        """Implements the abstract process() method."""
        parsed = self._extract_docstrings_and_functions()

        # Simple container object
        class Result:
            pass

        result = Result()
        result.module_doc = parsed.get("module_doc")
        result.functions = parsed.get("functions")
        return result
