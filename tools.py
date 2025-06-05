from langchain.tools import tool
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from smolagents import VisitWebpageTool, PythonInterpreterTool, SpeechToTextTool, Tool
from langchain_community.tools.google_serper.tool import GoogleSerperAPIWrapper
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()

duckduckgo = DuckDuckGoSearchRun()
python_repl = PythonREPL()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
# Instantiate smolagents tools
visit_webpage_tool = VisitWebpageTool()
python_interpreter_tool = PythonInterpreterTool()
speech_to_text_tool = SpeechToTextTool()
search_api = GoogleSerperAPIWrapper()


transcript_tool = Tool.from_space(
                    "maguid28/TranscriptTool",
                    name="TranscriptTool",
                    description="""
                    A smolagent tool for transcribing audio and video files into text. This tool utilises Whisper for transcription 
                    and ffmpeg for media conversion, enabling agents to process multimedia inputs into text. The tool supports robust 
                    file handling, including format conversion to WAV and dynamic device selection for optimal performance.
                    """
                )

@tool
def python_repl_tool(code: str) -> str:
    """
    Execute Python code in a REPL environment and return the output as a string.
    Args:
        code (str): The Python code to execute in the REPL.
    Returns:
        str: The output of the executed code from the REPL.
    """
    return python_repl.run(code)


@tool
def visit_webpage(url: str) -> str:
    """
    Visit a webpage and return its content as a string.
    Args:
        url (str): The URL of the webpage to visit.
    Returns:
        str: The content of the webpage.
    """
    return visit_webpage_tool(url=url)

@tool
def python_interpreter(code: str) -> str:
    """
    Execute Python code and return the output as a string.
    Args:
        code (str): The Python code to execute.
    Returns:
        str: The output of the executed code.
    """
    return python_interpreter_tool(code=code)

@tool
def speech_to_text(audio_path: str) -> str:
    """
    Convert speech in an audio file to text.
    Args:
        audio_path (str): The path to the audio file.
    Returns:
        str: The transcribed text from the audio.
    """
    return speech_to_text_tool(audio=audio_path)

@tool
def read_file_contents(file_path: str) -> str:
    """
    Read and return the contents of a file as a string.
    Args:
        file_path (str): The path to the file to read.
    Returns:
        str: The contents of the file, or an error message if the file cannot be read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def google_serper_search(query: str) -> str:
    """
    Search the web using Google Serper API and return the results as a string.
    Args:
        query (str): The search query string.
    Returns:
        str: The search results from Google Serper API.
    """
    return search_api.run(query)

@tool
def transcript_tool_langchain(audio_path: str) -> str:
    """
    Transcribe an audio or video file to text using the TranscriptTool from smolagents.
    Args:
        audio_path (str): The path to the audio or video file.
    Returns:
        str: The transcribed text from the file.
    Raises:
        FileNotFoundError: If the file does not exist at the given path.
    """
    import os
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")
    return transcript_tool(audio_path)

@tool
def youtube_transcript_tool(youtube_url_or_id: str) -> str:
    """
    Fetch the transcript of a YouTube video using its URL or video ID.
    Args:
        youtube_url_or_id (str): The YouTube video URL or video ID.
    Returns:
        str: The transcript of the video, or an error message if not available.
    """
    import re
    # Extract video ID from URL if needed
    video_id = youtube_url_or_id
    match = re.search(r"(?:v=|youtu.be/)([\w-]{11})", youtube_url_or_id)
    if match:
        video_id = match.group(1)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"