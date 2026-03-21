from django import template
from apps.ai_assistant.models import AIAssistantConfig

register = template.Library()


@register.simple_tag
def get_ai_name():
    """Mengembalikan nama AI dari konfigurasi."""
    try:
        config = AIAssistantConfig.load()
        return config.ai_name or 'AI Assistant'
    except Exception:
        return 'AI Assistant'
