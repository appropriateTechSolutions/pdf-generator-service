"""
Template Rendering Service using Jinja2
"""
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import logging

logger = logging.getLogger(__name__)

class TemplateRenderer:
    """Handles HTML template rendering with Jinja2"""
    
    def __init__(self, template_dir: str = None):
        """
        Initialize template renderer
        
        Args:
            template_dir: Directory containing templates (default: app/templates)
        """
        if template_dir is None:
            # Get the templates directory relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_dir = os.path.join(base_dir, 'template')
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        logger.info(f"Template renderer initialized with directory: {template_dir}")
    
    def render(self, template_name: str, context: dict) -> str:
        """
        Render template with given context
        
        Args:
            template_name: Name of the template file
            context: Dictionary of variables to pass to template
            
        Returns:
            Rendered HTML as string
            
        Raises:
            TemplateNotFound: If template doesn't exist
            Exception: If rendering fails
        """
        try:
            logger.info(f"Rendering template: {template_name}")
            
            template = self.env.get_template(template_name)
            html_content = template.render(**context)
            
            logger.info(f"Template rendered successfully: {template_name}")
            return html_content
            
        except TemplateNotFound:
            logger.error(f"Template not found: {template_name}")
            raise TemplateNotFound(f"Template '{template_name}' not found in {self.template_dir}")
        except Exception as e:
            logger.error(f"Failed to render template: {str(e)}")
            raise Exception(f"Template rendering failed: {str(e)}")
    
    def add_filter(self, name: str, func):
        """
        Add custom filter to Jinja2 environment
        
        Args:
            name: Filter name
            func: Filter function
        """
        self.env.filters[name] = func