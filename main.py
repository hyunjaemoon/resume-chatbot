import base64
import mesop as me

from chat import ChatMessage, chat, refresh_output
from resume_chatbot_agent import ResumeChatbotAgent


SIDENAV_WIDTH = 200
MAX_FILE_MB_SIZE = 5

PRIVACY_NOTICE = """
This page is powered by Google's Gemini AI model. By using this widget, you acknowledge that:

- Your messages will be processed by Google's AI services
- Messages are not stored permanently but are used in the current session
- Personal information should not be shared in conversations
- The AI may occasionally provide inaccurate information

For more information about Gemini's data handling, please visit [Gemini Apps Privacy Notice](https://support.google.com/gemini/answer/13594961?hl=en#privacy_notice).
"""

resume_chatbot_agent = ResumeChatbotAgent()


@me.stateclass
class State:
    file_uploaded: me.UploadedFile = None
    file_size_error: bool = False
    file_type_error: bool = False
    data_url: str = None
    history: tuple[tuple[str, str]] = ()
    acknowledgement: bool = False


def load(e: me.LoadEvent):
    me.set_theme_mode("dark")
    me.set_page_title("Resume Chatbot")


def handle_upload(e: me.UploadEvent):
    state = me.state(State)
    if e.file.size > MAX_FILE_MB_SIZE * 1024 * 1024:
        state.file_size_error = True
        return
    else:
        state.file_size_error = False
    if e.file.mime_type != "application/pdf":
        state.file_type_error = True
        return
    else:
        state.file_type_error = False
    state.file_uploaded = e.file
    state.data_url = _convert_contents_data_url(e.file)
    state.history = ()
    refresh_output()


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
    if state.file_type_error:
        with me.box(style=me.Style(margin=me.Margin.all(10))):
            me.text(f"File type must be a PDF. Please upload a PDF file.", style=me.Style(
                text_align="center"))


@me.page(
    on_load=load,
    path="/",
)
def app():
    state = me.state(State)
    if state.acknowledgement:
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
                chat(
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
    else:
        with me.box(
            style=me.Style(
                padding=me.Padding.all(15),
            ),
        ):
            with me.box(style=me.Style(margin=me.Margin.all(10))):
                me.link(text="Hyun Jae Moon Portfolio", url="https://hyunjaemoon.com",
                        style=me.Style(color=me.theme_var("primary")))
            me.text("Welcome to the Resume Chatbot!",
                    type="headline-2", style=me.Style(text_align="center"))
            me.markdown(PRIVACY_NOTICE)
            with me.box(style=me.Style(display="flex", flex_direction="row", gap=12)):
                me.button("I acknowledge and accept the privacy notice", type="flat",
                          on_click=lambda _: setattr(me.state(State), 'acknowledgement', True))


def _convert_contents_data_url(file: me.UploadEvent):
    return (
        f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
    )


def transform(input: str, history: list[ChatMessage]):
    state = me.state(State)
    response = resume_chatbot_agent.chat(input, state.data_url, state.history)
    state.history = state.history + [("user", input), ("assistant", response)]
    yield response
