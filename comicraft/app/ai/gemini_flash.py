from google import genai
from google.genai import types
from app.config import settings
from app.models import PromptRequest, OutlineResponse

def generate_outline(payload: PromptRequest) -> OutlineResponse:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")
    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f'''Create a coherent five-panel comic outline.
Story idea: {payload.story_prompt}
Character: {payload.character_name}
Setting: {payload.setting}
Tone: {payload.tone}
Art style: {payload.art_style}
Requirements: exactly five panels; preserve character identity; make scenes visually coherent; describe character, action, environment, camera, lighting and art style; no readable text/logos in images.'''
    response = client.models.generate_content(model=settings.gemini_outline_model, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=OutlineResponse))
    return OutlineResponse.model_validate_json(response.text)
