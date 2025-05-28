from vertexai.generative_models import Part, Content, GenerativeModel
import vertexai
import base64
import re

MODEL_NAME = "gemini-2.0-flash"

vertexai.init(project="resume-chatbot-generator", location="us-central1")


class ResumeChatbotAgent:
    def __init__(self):
        self.client = GenerativeModel(
            model_name=MODEL_NAME, 
            system_instruction="""
            You are a helpful assistant that can answer questions about the resume.
            Pretend you are the person in the resume.
            Please speak in the language of the user's question.
            User will always ask a question with the pdf file attached.
            """
        )

    def chat(self, message: str, data_url: str, history: list[str]) -> str:
        try:
            match = re.match(r'data:([^;]+);base64,(.+)', data_url)
            if match:
                mime_type, base64_data = match.groups()
                file_part = Part.from_data(
                    data=base64.b64decode(base64_data),
                    mime_type=mime_type
                )
            else:
                return "Error uploading resume"

            input_content = [] 
            
            for role, content in history:
                input_content.append(Content(
                    role=role,
                    parts=[Part.from_text(content)]
                ))
            
            content = Content(
                role="user",
                parts=[
                    file_part,
                    Part.from_text(message)
                ]
            )
            input_content.append(content)

            # Generate content using the model
            result = self.client.generate_content(input_content)
            return result.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
