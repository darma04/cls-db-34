/**
 * ==========================================================================
 *  PERMISSION MANAGEMENT - Kelola Permission (Hak Akses) via AJAX
 * ==========================================================================
 *  File ini menangani operasi CRUD untuk permission (hak akses) yang
 *  dikaitkan dengan role dan modul tertentu.
 *
 *  Fungsi utama:
 *  1. Tambah permission baru via modal form (Add Permission)
 *  2. Edit permission yang sudah ada via modal form (Edit Permission)
 *
 *  Alur kerja:
 *  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐
 *  │ User klik   │    │ Modal form   │    │ AJAX POST    │
 *  │ tombol      │───→│ muncul       │───→│ ke server    │
 *  │ Add/Edit    │    │ (Bootstrap)  │    │ Django view  │
 *  └─────────────┘    └──────────────┘    └──────────────┘
 *
 *  Terhubung dengan:
 *  - templates/access/permissions.html → Template halaman permission
 *  - apps/user_management/views.py → Django views untuk AJAX endpoint
 *  - apps/core/models.py → Model RolePermission di database
 *
 *  Dependensi:
 *  - Bootstrap 5 (Modal component) → Untuk popup form tambah/edit
 *  - SweetAlert2 (Swal) → Untuk notifikasi toast sukses/error
 * ==========================================================================
 */

// IIFE (Immediately Invoked Function Expression)
// Membungkus semua kode dalam fungsi anonim yang langsung dieksekusi
// Tujuan: Mencegah variabel & fungsi "bocor" ke scope global (window)
// Sehingga tidak bentrok dengan variabel/fungsi dari file JS lain
(function() {
    'use strict';  // Mode ketat — JavaScript akan error jika ada variabel tanpa deklarasi

    // ═══════════════════════════════════════════════════════
    // INISIALISASI — Jalankan saat halaman selesai dimuat
    // ═══════════════════════════════════════════════════════
    // DOMContentLoaded = event yang dipicu setelah seluruh HTML selesai di-parse
    // (tapi sebelum gambar/CSS selesai dimuat — lebih cepat dari 'load')
    document.addEventListener('DOMContentLoaded', function() {
        initializeAddPermissionModal();    // Setup modal tambah permission
        initializeEditPermissionModal();   // Setup modal edit permission
    });

    // ─────────────────────────────────────────────────────────
    // INISIALISASI MODAL TAMBAH PERMISSION
    // ─────────────────────────────────────────────────────────
    // Menghubungkan form tambah permission dengan handler submit AJAX.
    // Form ini ada di dalam Bootstrap modal #addPermissionModal.
    // ─────────────────────────────────────────────────────────
    function initializeAddPermissionModal() {
        // Cari elemen form berdasarkan ID
        const form = document.getElementById('addPermissionForm');
        if (!form) return;  // Jika form tidak ada di halaman ini, skip

        // Pasang event listener untuk submit form
        // preventDefault() mencegah reload halaman (submit biasa)
        // Lalu kirim data via AJAX (tanpa reload halaman)
        form.addEventListener('submit', function(e) {
            e.preventDefault();                         // Cegah submit bawaan browser
            handleAddPermissionSubmission(form);        // Kirim via AJAX
        });
    }

    // ─────────────────────────────────────────────────────────
    // HANDLER SUBMIT FORM TAMBAH PERMISSION
    // ─────────────────────────────────────────────────────────
    // Mengirim data form tambah permission ke server via AJAX POST.
    //
    // Alur:
    // 1. Validasi field wajib (role & module)
    // 2. Tampilkan loading spinner di tombol submit
    // 3. Kirim FormData via fetch() ke endpoint Django
    // 4. Tampilkan notifikasi sukses/error
    // 5. Reload halaman jika berhasil
    //
    // Parameter:
    //   form (HTMLFormElement) — Elemen form yang di-submit
    // ─────────────────────────────────────────────────────────
    function handleAddPermissionSubmission(form) {
        // FormData → objek bawaan browser yang otomatis mengumpulkan
        // semua nilai input dari form (termasuk checkbox, select, dll)
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;  // Simpan teks asli tombol untuk restore nanti

        // ─── VALIDASI ───
        // Cek field wajib: role dan module
        const role = formData.get('role');       // Ambil nilai dari <select name="role">
        const module = formData.get('module');   // Ambil nilai dari <select name="module">

        if (!role || !module) {
            // Tampilkan error jika field kosong
            Swal.fire('Error', 'Silakan pilih Role dan Modul', 'error');
            return;  // Hentikan proses
        }

        // ─── LOADING STATE ───
        // Disable tombol dan tampilkan spinner untuk mencegah double-submit
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating...';

        // ─── CSRF TOKEN ───
        // Cross-Site Request Forgery token — wajib untuk POST request di Django
        // Token ini dihasilkan oleh {% csrf_token %} di template HTML
        // Tanpa token ini, Django akan menolak request dengan error 403
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // ─── KIRIM REQUEST AJAX ───
        // Menggunakan fetch() API (bawaan browser modern, tanpa library tambahan)
        // POST ke endpoint Django untuk membuat permission baru
        fetch('/access/permissions/ajax/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,    // Header CSRF untuk autentikasi
            },
            body: formData                    // Data form yang akan dikirim
        })
        .then(response => response.json())     // Konversi response ke JSON
        .then(data => {
            if (data.success) {
                // ─── BERHASIL ───
                // Tampilkan notifikasi sukses
                showToast('success', data.message || 'Permission berhasil ditambahkan!');

                // Tutup modal Bootstrap
                const modalInstance = bootstrap.Modal.getInstance(document.getElementById('addPermissionModal'));
                modalInstance.hide();

                // Reload halaman setelah 1 detik (agar user sempat baca notifikasi)
                setTimeout(() => location.reload(), 1000);
            } else {
                // ─── GAGAL (dari server) ───
                // Tampilkan pesan error dari server
                showToast('error', data.message || 'Gagal menambahkan permission');
                // Kembalikan tombol ke keadaan semula
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        })
        .catch(error => {
            // ─── ERROR JARINGAN ───
            // Error terjadi jika: koneksi terputus, server mati, timeout, dll
            console.error('Error:', error);
            showToast('error', 'Terjadi kesalahan saat menambahkan permission');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        });
    }

    // ─────────────────────────────────────────────────────────
    // INISIALISASI MODAL EDIT PERMISSION
    // ─────────────────────────────────────────────────────────
    // Menghubungkan modal edit permission dengan:
    // 1. Event 'show.bs.modal' → load data permission saat modal dibuka
    // 2. Event 'submit' form → kirim perubahan ke server via AJAX
    // ─────────────────────────────────────────────────────────
    function initializeEditPermissionModal() {
        const modal = document.getElementById('editPermissionModal');
        const form = document.getElementById('editPermissionForm');

        if (!modal || !form) return;  // Skip jika elemen tidak ada

        // ─── EVENT MODAL DIBUKA ───
        // 'show.bs.modal' → event Bootstrap yang dipicu SAAT modal akan ditampilkan
        // event.relatedTarget → elemen (tombol) yang memicu pembukaan modal
        // Data permission ID diambil dari atribut data-permission-id di tombol
        modal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;  // Tombol yang diklik
            if (button) {
                // Ambil ID permission dari data attribute di tombol
                const permissionId = button.getAttribute('data-permission-id');
                if (permissionId) {
                    loadPermissionData(permissionId);  // Muat data dari server
                }
            }
        });

        // ─── EVENT SUBMIT FORM ───
        form.addEventListener('submit', function(e) {
            e.preventDefault();                        // Cegah submit bawaan
            handleEditPermissionSubmission(form);       // Kirim via AJAX
        });
    }

    // ─────────────────────────────────────────────────────────
    // MUAT DATA PERMISSION UNTUK EDIT
    // ─────────────────────────────────────────────────────────
    // Mengambil data permission dari server via AJAX GET
    // dan mengisi form edit dengan data tersebut.
    //
    // Alur:
    // 1. Tampilkan "Loading..." di form
    // 2. Fetch data dari endpoint Django
    // 3. Isi field form dengan data dari server
    // 4. Set checkbox sesuai izin yang dimiliki
    //
    // Parameter:
    //   permissionId (string) — ID permission di database
    // ─────────────────────────────────────────────────────────
    function loadPermissionData(permissionId) {
        // Referensi ke elemen-elemen form edit
        const permissionIdInput = document.getElementById('editPermissionId');
        const roleDisplay = document.getElementById('editPermissionRoleDisplay');
        const moduleDisplay = document.getElementById('editPermissionModuleDisplay');

        // Tampilkan loading text sementara data diambil
        if (roleDisplay) roleDisplay.textContent = 'Loading...';
        if (moduleDisplay) moduleDisplay.textContent = 'Loading...';

        // Fetch data permission dari server
        // Template literal `${}` digunakan untuk menyisipkan variabel ke URL
        fetch(`/access/permissions/ajax/${permissionId}/data/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const permission = data.permission;

                    // ─── ISI FIELD FORM ───
                    // Set ID permission di hidden input (untuk dikirim saat submit)
                    if (permissionIdInput) permissionIdInput.value = permission.id;
                    // Tampilkan nama role (hanya display, tidak bisa diedit)
                    if (roleDisplay) roleDisplay.textContent = permission.role_display;
                    // Tampilkan nama modul (hanya display, tidak bisa diedit)
                    if (moduleDisplay) moduleDisplay.textContent = permission.module_display;

                    // ─── SET CHECKBOX IZIN ───
                    // 4 checkbox CRUD: view, create, edit, delete
                    const viewCheck = document.getElementById('editCanView');
                    const createCheck = document.getElementById('editCanCreate');
                    const editCheck = document.getElementById('editCanEdit');
                    const deleteCheck = document.getElementById('editCanDelete');
                    const descInput = document.getElementById('editPermissionDescription');

                    // Centang/uncheck berdasarkan data dari server
                    if (viewCheck) viewCheck.checked = permission.can_view;
                    if (createCheck) createCheck.checked = permission.can_create;
                    if (editCheck) editCheck.checked = permission.can_edit;
                    if (deleteCheck) deleteCheck.checked = permission.can_delete;
                    // Isi deskripsi jika ada
                    if (descInput) descInput.value = permission.description || '';
                } else {
                    showToast('error', data.message || 'Gagal memuat data permission');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('error', 'Terjadi kesalahan saat memuat permission');
            });
    }

    // ─────────────────────────────────────────────────────────
    // HANDLER SUBMIT FORM EDIT PERMISSION
    // ─────────────────────────────────────────────────────────
    // Mengirim perubahan permission ke server via AJAX POST.
    // Alur sama dengan handleAddPermissionSubmission, tapi untuk update.
    //
    // Parameter:
    //   form (HTMLFormElement) — Elemen form edit yang di-submit
    // ─────────────────────────────────────────────────────────
    function handleEditPermissionSubmission(form) {
        const formData = new FormData(form);
        const permissionId = document.getElementById('editPermissionId').value;
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;

        // Loading state — disable tombol dan tampilkan spinner
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Updating...';

        // CSRF token untuk autentikasi request
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Kirim request AJAX POST ke endpoint update
        fetch(`/access/permissions/ajax/${permissionId}/edit/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Berhasil — tampilkan notifikasi dan reload
                showToast('success', data.message || 'Permission berhasil diupdate!');
                const modalInstance = bootstrap.Modal.getInstance(document.getElementById('editPermissionModal'));
                modalInstance.hide();
                setTimeout(() => location.reload(), 1000);
            } else {
                // Gagal — tampilkan error dan kembalikan tombol
                showToast('error', data.message || 'Gagal mengupdate permission');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        })
        .catch(error => {
            // Error jaringan
            console.error('Error:', error);
            showToast('error', 'Terjadi kesalahan saat mengupdate permission');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        });
    }

    // ─────────────────────────────────────────────────────────
    // SHOW TOAST — Tampilkan Notifikasi Pop-up
    // ─────────────────────────────────────────────────────────
    // Menampilkan notifikasi kecil (toast) di pojok kanan atas
    // menggunakan library SweetAlert2 (Swal).
    //
    // Jika SweetAlert2 tidak tersedia (misalnya gagal dimuat),
    // fallback ke alert() bawaan browser.
    //
    // Parameter:
    //   type (string) — Tipe notifikasi: 'success' atau 'error'
    //   message (string) — Pesan yang ditampilkan
    // ─────────────────────────────────────────────────────────
    function showToast(type, message) {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                icon: type === 'success' ? 'success' : 'error',  // Ikon: centang hijau atau silang merah
                title: type === 'success' ? 'Sukses!' : 'Error!', // Judul notifikasi
                text: message,                                      // Isi pesan
                timer: 3000,                                        // Otomatis tutup setelah 3 detik
                showConfirmButton: false,                           // Tanpa tombol OK
                toast: true,                                        // Mode toast (kecil, di pojok)
                position: 'top-end'                                 // Posisi: pojok kanan atas
            });
        } else {
            // Fallback jika SweetAlert2 tidak tersedia
            alert(message);
        }
    }

})();  // Akhir IIFE — langsung eksekusi fungsi anonim ini
