from vertexai.generative_models import Part, Content, GenerativeModel
import vertexai
import base64
import re
from typing import List
import mesop.labs as mel
MODEL_NAME = "gemini-2.0-flash"

vertexai.init(project="resume-chatbot-generator", location="us-central1")


class ResumeChatbotAgent:
    def __init__(self):
        self.client = GenerativeModel(
            model_name=MODEL_NAME, system_instruction="You are a helpful assistant that can answer questions about the resume. Pretend you are the person in the resume.")
        self.file = None
        self.history = []

    def upload_resume(self, file_path: str):
        # Check if the file_path is a data URL
        if file_path.startswith('data:'):
            # Extract the base64 data from the data URL
            match = re.match(r'data:([^;]+);base64,(.+)', file_path)
            if match:
                mime_type, base64_data = match.groups()
                # Create a Part from the base64 data
                self.file = Part.from_data(
                    data=base64.b64decode(base64_data),
                    mime_type=mime_type
                )
            else:
                raise ValueError("Invalid data URL format")
        else:
            # If it's a regular file path, use from_uri
            self.file = Part.from_uri(
                uri=file_path,
                mime_type="application/pdf",
            )

    def chat(self, message: str) -> str:
        if self.file is None:
            return "No resume file uploaded"

        try:         
            # Create a content object with both the file and the user's message
            content = Content(
                role="user",
                parts=[
                    self.file,
                    Part.from_text(message)
                ]
            )
            
            self.history.append(content)

            # Generate content using the model
            result = self.client.generate_content(self.history)
            result_content = Content(
                role="assistant",
                parts=[Part.from_text(result.text)]
            )
            self.history.append(result_content)
            return result.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
