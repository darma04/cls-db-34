"""
==========================================================================
 BOOTSTRAP LAYOUT VERTICAL - Inisialisasi Layout Vertikal
   ==========================================================================
   File Python untuk menginisialisasi context layout vertikal.
   Menyiapkan: sidebar menu, breadcrumb, template variables.
   Dipanggil oleh TemplateHelper untuk setiap request dengan layout vertikal.
"""

from django.conf import settings
import json


from web_project.template_helpers.theme import TemplateHelper

menu_file_path =  settings.BASE_DIR / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / "vertical_menu.json"

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in web_project/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        TemplateBootstrapLayoutVertical.init_menu_data(context)

        return context

    def init_menu_data(context):
        # Load the menu data from the JSON file
        menu_data = json.load(menu_file_path.open()) if menu_file_path.exists() else []
        
        # Get request from context (if available via request context processor)
        request = context.get('request')
        
        # Filter menu based on user permissions
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            menu_data = TemplateBootstrapLayoutVertical.filter_menu_by_permission(
                menu_data, request.user
            )

        # Updated context with menu_data
        context.update({ "menu_data": menu_data })
    
    def filter_menu_by_permission(menu_data, user):
        """
        Filter menu items based on user's role and permissions from the database.
        Uses RolePermission model to check if user has 'can_view' permission for each module.
        NOTE: 'allowed_roles' in menu JSON is IGNORED - only database permissions matter.
        """
        from apps.core.permissions import get_user_role, has_permission
        from django.conf import settings
        import os
        
        user_role = get_user_role(user)
        
        # DEBUG: Write to file for tracing
        debug_lines = []
        debug_lines.append(f'user={user.username} role={user_role}')
        debug_lines.append(f'profile.role raw={getattr(user.profile, "role", "NO_PROFILE") if hasattr(user, "profile") else "NO_PROFILE"}')
        
        # Also check what's in the DB for this role
        try:
            from apps.core.models import RolePermission
            all_perms = RolePermission.objects.filter(role__iexact=user_role)
            debug_lines.append(f'DB records for role {user_role}: {all_perms.count()}')
            for p in all_perms:
                debug_lines.append(f'  DB: role={p.role} module={p.module} view={p.can_view} create={p.can_create}')
        except Exception as e:
            debug_lines.append(f'DB error: {e}')
        
        # Superuser sees everything
        if user_role == 'SUPERUSER':
            debug_lines.append('SUPERUSER => show all')
            try:
                debug_path = str(settings.BASE_DIR / 'debug_sidebar.txt')
                with open(debug_path, 'w') as f:
                    f.write('\n'.join(debug_lines))
            except Exception:
                pass
            return menu_data
        
        # Mapping of menu slug to module permission name
        slug_to_module = {
            'dashboard': 'dashboard',
            'produk': 'produk',
            'inventory': 'inventory',
            'pembelian': 'pembelian',
            'penjualan': 'penjualan',
            'pos': 'pos',
            'invoice': 'pos',  # Invoice uses same module as POS
            'biaya': 'biaya',
            'hr': 'hr',
            'laporan': 'laporan',
            'users': 'user_management',
            'access-control': 'user_management',
            'activity-log': 'activity_log',
            'pengaturan': 'pengaturan',
            'automation': 'automation',
            'ai': 'ai',
        }
        
        filtered_menu = {"menu": []}
        
        for item in menu_data.get('menu', []):
            # Menu headers are always shown (we'll filter after)
            if 'menu_header' in item:
                filtered_menu['menu'].append(item)
                continue
            
            slug = item.get('slug', '')
            
            # Check if user has permission for this module
            module_name = slug_to_module.get(slug, slug)
            
            # Check permission from database ONLY - ignore 'allowed_roles' from JSON
            perm_result = has_permission(user, 'read', module_name)
            debug_lines.append(f'slug={slug} => module={module_name} => perm={perm_result}')
            if perm_result:
                filtered_menu['menu'].append(item)
            # If no permission, skip this menu item
        
        # Remove orphan menu headers (headers with no items following)
        cleaned_menu = {"menu": []}
        i = 0
        menu_items = filtered_menu['menu']
        
        while i < len(menu_items):
            item = menu_items[i]
            
            if 'menu_header' in item:
                # Check if there's at least one non-header item after this header
                has_content = False
                j = i + 1
                while j < len(menu_items):
                    if 'menu_header' in menu_items[j]:
                        break  # Found next header, no content for current header
                    else:
                        has_content = True
                        break
                
                if has_content:
                    cleaned_menu['menu'].append(item)
            else:
                cleaned_menu['menu'].append(item)
            
            i += 1
        
        # DEBUG: Write debug info to file
        try:
            debug_path = str(settings.BASE_DIR / 'debug_sidebar.txt')
            debug_lines.append(f'filtered_items={len(filtered_menu["menu"])} cleaned_items={len(cleaned_menu["menu"])}')
            with open(debug_path, 'w') as f:
                f.write('\n'.join(debug_lines))
        except Exception:
            pass
        
        return cleaned_menu
