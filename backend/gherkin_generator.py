import os
from openai import OpenAI
from dotenv import load_dotenv  # ✅ import dotenv

class GherkinGeneratorHybrid:
    def __init__(self, code_text: str, requirement_text: str, filename: str):
        # Load .env file
        load_dotenv()

        self.code_text = code_text
        self.requirement_text = requirement_text
        self.filename = filename

        # ✅ Read API key securely from environment
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found. Please set it in your .env file.")

        # Initialize client
        self.client = OpenAI(api_key=self.api_key)

    def process(self):
        prompt = f"""
        You are an expert in BDD (Behavior Driven Development).
        Using the following:
        1. Python source code (implementation details)
        2. Requirement document (business rules)
        
        Generate a clear, well-structured Gherkin feature file (.feature)
        that includes realistic scenarios, examples, and proper Given/When/Then steps.

        ---
        📘 Requirement Document:
        {self.requirement_text}

        ---
        💻 Python Code:
        {self.code_text}

        Output only valid Gherkin syntax.
        """

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output[0].content[0].text.strip()
