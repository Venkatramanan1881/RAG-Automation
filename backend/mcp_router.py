from utils.file_utils import detect_file_types
from utils.transcriber import transcribe_audio
from utils.ocr import extract_text_from_image_or_pdf
from langgraph_interface import run_langgraph_pipeline


async def process_user_message(user_input: str) -> str:
    """
    Process the user input and return the response from LangGraph.
    """

    if not user_input:
        return "No input provided"
    # Call the LangGraph pipeline with the user input
    response = await run_langgraph_pipeline(user_input)
    
    return response