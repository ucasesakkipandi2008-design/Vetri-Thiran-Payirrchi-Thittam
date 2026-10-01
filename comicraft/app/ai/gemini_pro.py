from google import genai
from google.genai import types
from app.config import settings
from app.models import PromptRequest, OutlineResponse, StoryResponse

def generate_story(payload: PromptRequest, outline: OutlineResponse) -> StoryResponse:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")
    client = genai.Client(api_key=settings.gemini_api_key)
    outline_text = "\n".join(f"Panel {p.panel_number}: {p.scene}" for p in outline.panels)
    prompt = f'''Write dialogue, captions and narration for this five-panel comic.
Story idea: {payload.story_prompt}
Character: {payload.character_name}
Tone: {payload.tone}
Outline:
{outline_text}
Requirements: exactly one story object per panel; preserve sequence; short natural dialogue; concise captions.'''
    response = client.models.generate_content(model=settings.gemini_story_model, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=StoryResponse))
    return StoryResponse.model_validate_json(response.text)
