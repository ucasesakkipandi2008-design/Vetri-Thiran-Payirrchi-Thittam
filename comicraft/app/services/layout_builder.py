from app.models import OutlineResponse, StoryResponse, ComicPanel

def build_comic_layout(outline: OutlineResponse, story: StoryResponse, image_paths: list[str]) -> list[ComicPanel]:
    story_by_panel = {p.panel_number: p for p in story.panels}
    result = []
    for i, p in enumerate(outline.panels[:len(image_paths)]):
        s = story_by_panel.get(p.panel_number)
        result.append(ComicPanel(panel_number=p.panel_number, scene=p.scene, image_url=image_paths[i], narration=s.narration if s else "", caption=s.caption if s else "", dialogue=s.dialogue if s else ""))
    return result
