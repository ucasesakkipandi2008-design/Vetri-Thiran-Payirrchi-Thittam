from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=3)
    character_name: str = "Alex"
    setting: str = "A futuristic city"
    tone: str = "Adventure"
    art_style: str = "Comic book"

class PanelOutline(BaseModel):
    panel_number: int
    scene: str
    image_prompt: str

class OutlineResponse(BaseModel):
    title: str
    panels: list[PanelOutline]

class PanelStory(BaseModel):
    panel_number: int
    narration: str
    caption: str
    dialogue: str

class StoryResponse(BaseModel):
    title: str
    panels: list[PanelStory]

class ComicPanel(BaseModel):
    panel_number: int
    scene: str
    image_url: str
    narration: str
    caption: str
    dialogue: str

class ComicResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_path: str | None = None
