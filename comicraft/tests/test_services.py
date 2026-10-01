from app.models import OutlineResponse, PanelOutline, StoryResponse, PanelStory
from app.services.layout_builder import build_comic_layout

def test_layout_builder():
    outline = OutlineResponse(title="Test", panels=[PanelOutline(panel_number=1, scene="Scene", image_prompt="Image")])
    story = StoryResponse(title="Test", panels=[PanelStory(panel_number=1, narration="N", caption="C", dialogue="D")])
    result = build_comic_layout(outline, story, ["/static/panels/test.png"])
    assert result[0].dialogue == "D"
