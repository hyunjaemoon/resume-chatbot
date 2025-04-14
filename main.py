import base64
import mesop as me
import mesop.labs as mel

from resume_chatbot_agent import ResumeChatbotAgent


SIDENAV_WIDTH = 200
MAX_FILE_MB_SIZE = 5

resume_chatbot_agent = ResumeChatbotAgent()


@me.stateclass
class State:
    file_uploaded: me.UploadedFile = None
    file_size_error: bool = False


def load(e: me.LoadEvent):
    me.set_theme_mode("dark")
    me.set_page_title("Resume Chatbot")


def handle_upload(e: me.UploadEvent):
    state = me.state(State)
    if e.file.size > MAX_FILE_MB_SIZE * 1024 * 1024:
        state.file_size_error = True
        return
    resume_chatbot_agent.upload_resume(_convert_contents_data_url(e.file))
    state.file_uploaded = e.file
    state.file_size_error = False


def upload_component():
    state = me.state(State)
    with me.box(style=me.Style(display="flex", justify_content="center", align_items="center", align_content="center", align_self="center", padding=me.Padding.all(20))):
        with me.content_uploader(
            accepted_file_types=["application/pdf"],
            on_upload=handle_upload,
            type="flat",
            color="warn",
            style=me.Style(font_weight="bold"),
        ):
            me.icon("upload")
        if state.file_uploaded:
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.text(f"File name: {state.file_uploaded.name}")
                me.text(f"File size: {state.file_uploaded.size}")
                me.text(f"File type: {state.file_uploaded.mime_type}")
    if state.file_size_error:
        with me.box(style=me.Style(margin=me.Margin.all(10))):
            me.text(f"File size exceeds {MAX_FILE_MB_SIZE}MB limit. Please upload a smaller file.", style=me.Style(
                text_align="center"))


@me.page(
    on_load=load,
    path="/",
)
def app():
    state = me.state(State)
    with me.box(
        style=me.Style(
            padding=me.Padding.all(15),
        ),
    ):
        with me.box(style=me.Style(margin=me.Margin.all(10))):
            me.link(text="Hyun Jae Moon Portfolio", url="https://hyunjaemoon.com",
                    style=me.Style(color=me.theme_var("primary")))
        if state.file_uploaded:
            upload_component()
            mel.chat(
                transform, title=f"Resume Chatbot - {state.file_uploaded._name}", bot_user="Resume Chatbot")
        else:
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.text("Welcome to the Resume Chatbot!",
                        type="headline-2", style=me.Style(text_align="center"))
                me.text("Please upload your resume to get started.",
                        style=me.Style(text_align="center"))
                me.text(f"File must be a PDF under {MAX_FILE_MB_SIZE}MB.",
                        style=me.Style(text_align="center"))
                upload_component()


def _convert_contents_data_url(file: me.UploadEvent):
    return (
        f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
    )


def transform(input: str, history: list[mel.ChatMessage]):
    response = resume_chatbot_agent.chat(input)
    yield response
