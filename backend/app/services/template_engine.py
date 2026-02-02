"""Template engine for loading and managing resume templates."""

import json
import os
from typing import Dict, List
from pathlib import Path


class TemplateEngine:
    """Manage and load resume templates."""
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize template engine.
        
        Args:
            templates_dir: Directory containing template JSON files
        """
        if templates_dir is None:
            # Default to backend/templates directory
            current_dir = Path(__file__).parent.parent.parent
            templates_dir = current_dir / "templates"
        
        self.templates_dir = Path(templates_dir)
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all templates from JSON files."""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template_id = template_data.get('id')
                    if template_id:
                        self.templates[template_id] = template_data
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")
    
    def get_template(self, template_id: str) -> Dict:
        """
        Get a template by ID.
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template configuration dictionary
        """
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[Dict]:
        """
        List all available templates.
        
        Returns:
            List of template dictionaries
        """
        return list(self.templates.values())
    
    def template_exists(self, template_id: str) -> bool:
        """Check if a template exists."""
        return template_id in self.templates
