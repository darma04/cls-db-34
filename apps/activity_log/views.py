"""
Views untuk Log Aktifitas - Menampilkan riwayat aktivitas user.
"""
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_project import TemplateLayout
from .models import UserActivity


class ActivityLogIndexView(LoginRequiredMixin, ListView):
    model = UserActivity
    template_name = 'activity_log/index.html'
    context_object_name = 'activities'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related('user')
        # Filter berdasarkan aksi
        action = self.request.GET.get('action')
        if action:
            qs = qs.filter(action=action)
        # Filter berdasarkan user
        user_id = self.request.GET.get('user')
        if user_id:
            qs = qs.filter(user_id=user_id)
        # Filter berdasarkan tanggal
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        # Filter pencarian
        search = self.request.GET.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(description__icontains=search) |
                Q(model_name__icontains=search) |
                Q(object_repr__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        from django.contrib.auth.models import User
        context['users'] = User.objects.all().order_by('username')
        context['action_choices'] = UserActivity.ACTION_CHOICES
        context['total_activities'] = UserActivity.objects.count()
        context['filter_action'] = self.request.GET.get('action', '')
        context['filter_user'] = self.request.GET.get('user', '')
        context['filter_date_from'] = self.request.GET.get('date_from', '')
        context['filter_date_to'] = self.request.GET.get('date_to', '')
        context['filter_search'] = self.request.GET.get('search', '')
        return context
