"""
==========================================================================
 CORE TAGS - Template Tags & Filters untuk Pengecekan Permission
==========================================================================
 Custom template tags yang bisa dipanggil di template HTML:

 Filter:
 - {{ user|has_module_permission:'produk:read' }} → True/False

 Tag:
 - {% user_can 'read' 'produk' as can_view %}   → Simpan ke variabel

 Cara pakai di template:
 1. {% load core_tags %}                   ← Wajib dimuat dulu
 2. {% if user|has_module_permission:'produk:read' %}...{% endif %}
 3. {% user_can 'create' 'inventory' as can_add %}{% if can_add %}...{% endif %}

 Terhubung dengan:
 - core/permissions.py → has_permission() (logika pengecekan inti)
==========================================================================
"""
from django import template
from apps.core.permissions import has_permission

register = template.Library()  # Registry untuk mendaftarkan tags ke Django template engine


@register.filter(name='has_module_permission')
def has_module_permission_filter(user, module_and_action):
    """
    Template filter untuk check user permission.
    
    Usage in template:
        {% load core_tags %}
        {{ request.user|has_module_permission:'produk:read' }}
        {{ request.user|has_module_permission:'inventory:create' }}
    
    Args:
        user: Django User object
        module_and_action: String format 'module_name:action' 
                          e.g., 'produk:read', 'inventory:create'
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    try:
        module, action = str(module_and_action).split(':', 1)
        return has_permission(user, action, module)
    except (ValueError, AttributeError):
        return False


@register.simple_tag(takes_context=True)
def user_can(context, action, module):
    """
    Template tag untuk check user permission dengan syntax yang lebih clean.
    
    Usage in template:
        {% load core_tags %}
        {% user_can 'read' 'produk' as can_view %}
        {% if can_view %}...{% endif %}
        
        Or direct:
        {% if user_can 'update' 'inventory' %}...{% endif %}
    
    Args:
        context: Template context (auto-provided)
        action: Permission action ('read', 'create', 'update', 'delete')
        module: Module name ('produk', 'inventory', etc.)
    
    Returns:
        bool: True if user has permission
    """
    request = context.get('request')
    if not request or not request.user or not request.user.is_authenticated:
        return False
    
    return has_permission(request.user, action, module)
