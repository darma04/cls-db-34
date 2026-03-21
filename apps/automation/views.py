"""
Views untuk Automation (Telegram) - Pengaturan, Template Pesan, Log Notifikasi.
"""
import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from web_project import TemplateLayout
from .models import PengaturanTelegram, TemplatePesan, LogNotifikasi
from .telegram_service import kirim_pesan_telegram


class PengaturanTelegramView(LoginRequiredMixin, TemplateView):
    template_name = 'automation/pengaturan_telegram.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['pengaturan'] = PengaturanTelegram.load()
        context['total_terkirim'] = LogNotifikasi.objects.filter(status='sukses').count()
        context['total_gagal'] = LogNotifikasi.objects.filter(status='gagal').count()
        context['log_terbaru'] = LogNotifikasi.objects.all()[:5]
        return context

    def post(self, request, *args, **kwargs):
        pengaturan = PengaturanTelegram.load()
        pengaturan.bot_token = request.POST.get('bot_token', '').strip()
        pengaturan.chat_id = request.POST.get('chat_id', '').strip()
        pengaturan.aktif = request.POST.get('aktif') == 'on'
        pengaturan.notif_aktivasi = request.POST.get('notif_aktivasi') == 'on'
        pengaturan.notif_kadaluarsa = request.POST.get('notif_kadaluarsa') == 'on'
        pengaturan.notif_pembelian = request.POST.get('notif_pembelian') == 'on'
        pengaturan.notif_suspend = request.POST.get('notif_suspend') == 'on'
        pengaturan.save()
        messages.success(request, 'Pengaturan Telegram berhasil disimpan!')
        return redirect('automation:pengaturan_telegram')


class TemplatePesanListView(LoginRequiredMixin, ListView):
    model = TemplatePesan
    template_name = 'automation/template_pesan_list.html'
    context_object_name = 'templates'
    ordering = ['jenis']

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        for jenis, label in TemplatePesan.JENIS_CHOICES:
            TemplatePesan.get_template(jenis)
        context['templates'] = TemplatePesan.objects.all().order_by('jenis')
        return context


class TemplatePesanUpdateView(LoginRequiredMixin, UpdateView):
    model = TemplatePesan
    template_name = 'automation/template_pesan_form.html'
    fields = ['nama', 'template_pesan', 'aktif']
    success_url = reverse_lazy('automation:template_pesan_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        variabel_map = {
            'aktivasi': ['license_key', 'product_name', 'client_name', 'domain', 'expires_at'],
            'kadaluarsa': ['license_key', 'product_name', 'client_name', 'expires_at'],
            'pembelian': ['nomor_transaksi', 'client_name', 'product_name', 'total', 'tanggal'],
            'suspend': ['license_key', 'product_name', 'client_name'],
        }
        context['variabel_tersedia'] = variabel_map.get(self.object.jenis, [])
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Template "{form.instance.nama}" berhasil diupdate!')
        return super().form_valid(form)


class LogNotifikasiView(LoginRequiredMixin, ListView):
    model = LogNotifikasi
    template_name = 'automation/log_notifikasi.html'
    context_object_name = 'logs'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        jenis = self.request.GET.get('jenis')
        if jenis:
            qs = qs.filter(jenis_transaksi=jenis)
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['total_sukses'] = LogNotifikasi.objects.filter(status='sukses').count()
        context['total_gagal'] = LogNotifikasi.objects.filter(status='gagal').count()
        context['total_semua'] = LogNotifikasi.objects.count()
        context['jenis_filter'] = self.request.GET.get('jenis', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


@login_required
def test_kirim_telegram(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    pengaturan = PengaturanTelegram.load()
    if not pengaturan.bot_token or not pengaturan.chat_id:
        return JsonResponse({'success': False, 'message': 'Bot Token dan Chat ID harus diisi!'})
    pesan_test = (
        "✅ *Test Koneksi Berhasil!*\n"
        "━━━━━━━━━━━━━━━\n"
        "🤖 Bot Telegram terhubung dengan Central License Server\n"
        "📊 Notifikasi otomatis siap digunakan\n\n"
        "Pengaturan Aktif:\n"
        f"  • Aktivasi Lisensi: {'✅' if pengaturan.notif_aktivasi else '❌'}\n"
        f"  • Kadaluarsa: {'✅' if pengaturan.notif_kadaluarsa else '❌'}\n"
        f"  • Pembelian: {'✅' if pengaturan.notif_pembelian else '❌'}\n"
        f"  • Suspend: {'✅' if pengaturan.notif_suspend else '❌'}\n"
    )
    success, response = kirim_pesan_telegram(pengaturan.bot_token, pengaturan.chat_id, pesan_test)
    LogNotifikasi.objects.create(
        jenis_transaksi='aktivasi', nomor_referensi='TEST', pesan=pesan_test,
        status='sukses' if success else 'gagal',
        respons=json.dumps(response) if isinstance(response, dict) else None,
        error_message=response if not success and isinstance(response, str) else None,
    )
    if success:
        return JsonResponse({'success': True, 'message': 'Pesan test berhasil dikirim!'})
    return JsonResponse({'success': False, 'message': f'Gagal mengirim: {response}'})


@login_required
def deteksi_chat_id(request):
    import urllib.request
    import urllib.error
    import ssl
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    pengaturan = PengaturanTelegram.load()
    if not pengaturan.bot_token:
        return JsonResponse({'success': False, 'message': 'Bot Token harus diisi!'})
    bot_token = pengaturan.bot_token.strip()
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates?limit=10&offset=-10"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
        if result.get('ok') and result.get('result'):
            chat_ids_found = []
            for update in result['result']:
                msg = update.get('message') or update.get('channel_post') or {}
                chat = msg.get('chat', {})
                chat_id = chat.get('id')
                chat_title = chat.get('title') or chat.get('first_name') or str(chat_id)
                if chat_id:
                    entry = {'chat_id': str(chat_id), 'title': chat_title, 'type': chat.get('type', '')}
                    if not any(c['chat_id'] == entry['chat_id'] for c in chat_ids_found):
                        chat_ids_found.append(entry)
            if chat_ids_found:
                return JsonResponse({
                    'success': True,
                    'message': f'Chat ID ditemukan: {chat_ids_found[0]["chat_id"]} ({chat_ids_found[0]["title"]})',
                    'chat_id': chat_ids_found[0]['chat_id'],
                    'all_chats': chat_ids_found
                })
            return JsonResponse({'success': False, 'message': 'Tidak ditemukan pesan. Kirim /start ke bot terlebih dahulu.'})
        return JsonResponse({'success': False, 'message': 'Bot belum menerima pesan.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


@login_required
def reset_template(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    template = get_object_or_404(TemplatePesan, pk=pk)
    template.template_pesan = TemplatePesan._get_default_template(template.jenis)
    template.save()
    messages.success(request, f'Template "{template.nama}" berhasil direset!')
    return redirect('automation:template_pesan_list')
