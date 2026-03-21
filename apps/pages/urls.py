"""
==========================================================================
 PAGES URLS - Routing Halaman Statis (Error, Maintenance, dll)
==========================================================================
 URL routing untuk halaman-halaman statis/misc.
 Semua menggunakan MiscPagesView dengan template_name berbeda-beda.

 Peta URL:
 - /pages/misc/error/              → Halaman error
 - /pages/misc/under_maintenance/  → Halaman sedang maintenance
 - /pages/misc/comingsoon/         → Halaman coming soon
 - /pages/misc/not_authorized/     → Halaman tidak punya akses (403)
 - /pages/misc/server_error/       → Halaman server error (500)
==========================================================================
"""
from django.urls import path
from .views import MiscPagesView


urlpatterns = [
    # ── Halaman Error / Misc ─────────────────────────────────
    path(
        "pages/misc/error/",
        MiscPagesView.as_view(template_name="pages_misc_error.html"),
        name="pages-misc-error",
    ),
    path(
        "pages/misc/under_maintenance/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="pages-misc-under-maintenance",
    ),
    path(
        "pages/misc/comingsoon/",
        MiscPagesView.as_view(template_name="pages_misc_comingsoon.html"),
        name="pages-misc-comingsoon",
    ),
    path(
        "pages/misc/not_authorized/",
        MiscPagesView.as_view(template_name="pages_misc_not_authorized.html"),
        name="pages-misc-not-authorized",
    ),
    path(
        "pages/misc/server_error/",
        MiscPagesView.as_view(template_name="pages_misc_server_error.html"),
        name="pages-misc-server-error",
    ),
]
