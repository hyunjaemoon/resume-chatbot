import base64
import mesop as me
import mesop.labs as mel

from resume_chatbot_agent import ResumeChatbotAgent


SIDENAV_WIDTH = 200

resume_chatbot_agent = ResumeChatbotAgent()


@me.stateclass
class State:
    file_uploaded: me.UploadedFile = None


def load(e: me.LoadEvent):
    me.set_theme_mode("system")


def handle_upload(e: me.UploadEvent):
    state = me.state(State)
    resume_chatbot_agent.upload_resume(_convert_contents_data_url(e.file))
    state.file_uploaded = e.file


def upload_component():
    state = me.state(State)
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
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.image(src=_convert_contents_data_url(
                    state.file_uploaded))


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
            me.link(text="Hyun Jae Moon Portfolio", url="https://hyunjaemoon.com", style=me.Style(color=me.theme_var("primary")))
        if state.file_uploaded:
            upload_component()
            mel.chat(
                transform, title=f"Resume Chatbot - {state.file_uploaded._name}", bot_user="Resume Chatbot")
        else:
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.text("Welcome to the Resume Chatbot!", type="headline-2")
                me.text("Please upload your resume to get started. File must be a PDF.")
                upload_component()


def _convert_contents_data_url(file: me.UploadEvent):
    return (
        f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
    )


def transform(input: str, history: list[mel.ChatMessage]):
    response = resume_chatbot_agent.chat(input)
    yield response
