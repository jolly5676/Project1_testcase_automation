from backend.base_parser import CodeArtifact
from backend.code_parser import PythonCodeParser
from openai import OpenAI


class RequirementsGenerator(CodeArtifact):
    """Generates a structured requirements document from Python code."""

    def __init__(self, py_code: str, filename: str):
        super().__init__(py_code, filename)

        # ✅ Define your OpenAI API key here (replace with your own)
     

        # Initialize parser and OpenAI client
        self.parser = PythonCodeParser(py_code, filename)
        self.client = OpenAI(api_key=self.api_key)

    def _prompt(self):
        """Prepare prompt for generating a requirements document."""
        parsed = self.parser.process()

        # ✅ Normalize parser output (avoid .get() on non-dict objects)
        if not isinstance(parsed, dict):
            parsed = {
                "module_doc": getattr(parsed, "module_doc", "No module description provided."),
                "functions": getattr(parsed, "functions", []),
            }

        module_doc = parsed.get("module_doc", "No module description provided.")
        functions = parsed.get("functions", [])

        return f"""
        You are a senior business analyst.
        Generate a detailed, structured requirements specification document
        from the following Python module.

        ### Module Description:
        {module_doc}

        ### Functions and Logic:
        {functions}
        """

    def process(self):
        """Generate requirements document using OpenAI GPT."""
        response = self.client.responses.create(
            model="gpt-4.1",
            input=[
                {"role": "system", "content": "You are an expert requirements document writer."},
                {"role": "user", "content": self._prompt()},
            ]
        )
        return response.output[0].content[0].text.strip()
