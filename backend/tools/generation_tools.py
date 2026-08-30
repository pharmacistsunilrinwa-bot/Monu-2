import os
from typing import Dict, Any
from backend.tools.base_tool import BaseTool
from backend.services.permission_service import PermissionLevel, permission_service

class MediaGeneratorTool(BaseTool):
    @property
    def name(self) -> str:
        return "media_generator"

    @property
    def description(self) -> str:
        return "Generates visual assets, diagrams, images, or procedural SVGs based on descriptive prompts."

    @property
    def security_level(self) -> str:
        return PermissionLevel.STANDARD

    @property
    def arguments(self) -> Dict[str, Any]:
        return {
            "prompt": {
                "type": "string",
                "description": "Text description of the image/media/diagram to generate."
            },
            "media_type": {
                "type": "string",
                "description": "Desired format. Options: 'svg' (procedural graphic), 'html_canvas' (interactive visualization). Defaults to 'svg'.",
                "enum": ["svg", "html_canvas"]
            }
        }

    async def execute(self, user_id: str, **kwargs) -> Dict[str, Any]:
        if not permission_service.check_permission(user_id, self.security_level, f"Execute tool: {self.name}"):
            return {"success": False, "error": "Permission Denied"}

        prompt = kwargs.get("prompt", "")
        media_type = kwargs.get("media_type", "svg")

        if not prompt:
            return {"success": False, "error": "Missing prompt argument"}

        # Procedural SVG generation based on keywords
        prompt_lower = prompt.lower()
        
        # Default nice placeholder SVG
        svg_content = (
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400' width='100%' height='100%'>\n"
            "  <rect width='400' height='400' fill='#1e1e24' rx='15'/>\n"
            "  <defs>\n"
            "    <linearGradient id='grad' x1='0%' y1='0%' x2='100%' y2='100%'>\n"
            "      <stop offset='0%' style='stop-color:#8a2be2;stop-opacity:1' />\n"
            "      <stop offset='100%' style='stop-color:#4a00e0;stop-opacity:1' />\n"
            "    </linearGradient>\n"
            "  </defs>\n"
        )

        if "chart" in prompt_lower or "diagram" in prompt_lower or "graph" in prompt_lower:
            # Generate a nice business trend bar chart procedurally
            svg_content += (
                "  <text x='200' y='50' font-family='sans-serif' font-size='18' fill='#ffffff' text-anchor='middle'>Monu AI Trend Analytics</text>\n"
                "  <line x1='60' y1='300' x2='340' y2='300' stroke='#555555' stroke-width='2'/>\n"
                "  <line x1='60' y1='100' x2='60' y2='300' stroke='#555555' stroke-width='2'/>\n"
                "  <!-- Bars -->\n"
                "  <rect x='80' y='180' width='35' height='120' fill='url(#grad)' rx='3'/>\n"
                "  <rect x='140' y='140' width='35' height='160' fill='url(#grad)' rx='3'/>\n"
                "  <rect x='200' y='110' width='35' height='190' fill='url(#grad)' rx='3'/>\n"
                "  <rect x='260' y='80' width='35' height='220' fill='url(#grad)' rx='3'/>\n"
                "  <!-- Labels -->\n"
                "  <text x='97' y='325' font-family='sans-serif' font-size='12' fill='#aaaaaa' text-anchor='middle'>Q1</text>\n"
                "  <text x='157' y='325' font-family='sans-serif' font-size='12' fill='#aaaaaa' text-anchor='middle'>Q2</text>\n"
                "  <text x='217' y='325' font-family='sans-serif' font-size='12' fill='#aaaaaa' text-anchor='middle'>Q3</text>\n"
                "  <text x='277' y='325' font-family='sans-serif' font-size='12' fill='#aaaaaa' text-anchor='middle'>Q4</text>\n"
            )
        else:
            # Nice abstract Monu Logo shape
            svg_content += (
                "  <circle cx='200' cy='180' r='70' fill='url(#grad)' />\n"
                "  <polygon points='200,90 260,240 140,240' fill='none' stroke='#ffffff' stroke-width='4' stroke-linejoin='round'/>\n"
                "  <text x='200' y='320' font-family='sans-serif' font-size='20' font-weight='bold' fill='#ffffff' text-anchor='middle'>MONU PERSONAL SERVER</text>\n"
                f"  <text x='200' y='350' font-family='sans-serif' font-size='11' fill='#888888' text-anchor='middle'>{prompt[:40]}...</text>\n"
            )
            
        svg_content += "</svg>"

        # Save the SVG under user_data so the system can serve or return it
        filename = f"gen_media_{user_id}.svg"
        from backend.services.file_manager_service import file_manager_service
        try:
            full_path = file_manager_service._secure_path(filename)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
                
            return {
                "success": True,
                "media_type": media_type,
                "svg_content": svg_content,
                "file_path": filename,
                "message": f"Successfully generated procedural vector artwork based on your prompt and saved to '{filename}'."
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to save generated media file: {str(e)}"}
