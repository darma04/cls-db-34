/**
 * ==========================================================================
 *  MODAL ADD ROLE - Handler untuk Menambah Role Baru dengan Permission
 * ==========================================================================
 *  File ini menangani pembuatan role baru melalui modal popup.
 *
 *  Fitur:
 *  1. Checkbox "Select All" — centang/uncentang semua permission sekaligus
 *  2. Form submission via AJAX — kirim data role baru ke server
 *  3. Reset form saat modal ditutup — bersihkan semua input
 *
 *  Alur kerja penambahan role:
 *  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
 *  │ User klik    │    │ Modal muncul │    │ User isi     │    │ AJAX POST    │
 *  │ "Tambah Role"│───→│ (Bootstrap)  │───→│ nama + ceklis│───→│ ke server    │
 *  └──────────────┘    └──────────────┘    │ permission   │    └──────────────┘
 *                                          └──────────────┘
 *
 *  Terhubung dengan:
 *  - templates/access/roles.html → Template yang memuat modal dan file ini
 *  - apps/user_management/views.py → Endpoint AJAX /access/roles/ajax/create/
 *  - apps/core/models.py → Model RolePermission yang disimpan
 *
 *  Dependensi:
 *  - Bootstrap 5 (Modal) → Popup form
 *  - SweetAlert2 (Swal) → Notifikasi toast
 *
 *  Catatan teknis:
 *  - Menggunakan event delegation (document.addEventListener) agar event
 *    tetap bekerja meskipun elemen checkbox di-render secara dinamis
 *    (bukan dari HTML awal, tapi ditambahkan via JavaScript)
 * ==========================================================================
 */

// IIFE — membungkus kode agar tidak mencemari scope global
(function() {
    'use strict';  // Mode ketat JavaScript

    // ═══════════════════════════════════════════════════════
    // INISIALISASI — Pasang event listener setelah DOM siap
    // ═══════════════════════════════════════════════════════
    document.addEventListener('DOMContentLoaded', function() {

        // ─── EVENT DELEGATION: SELECT ALL CHECKBOX ───
        // Event delegation = memasang listener di PARENT (document),
        // bukan di elemen itu sendiri. Keuntungan:
        // - Tetap bekerja untuk elemen yang ditambahkan SETELAH halaman dimuat
        // - Lebih efisien daripada memasang listener di setiap checkbox
        document.addEventListener('change', function(e) {
            // Cek apakah yang berubah adalah checkbox "Select All"
            if (e.target && e.target.id === 'selectAll') {
                handleSelectAllChange(e.target);
            }
            // Cek apakah yang berubah adalah checkbox permission individual
            // Jika ya, update status checkbox "Select All" (centang/uncentang/indeterminate)
            if (e.target && e.target.classList.contains('permission-checkbox')) {
                updateSelectAllState();
            }
        });

        // ─── EVENT DELEGATION: FORM SUBMISSION ───
        // Menangkap event submit dari form tambah role
        document.addEventListener('submit', function(e) {
            if (e.target && e.target.id === 'addRoleForm') {
                e.preventDefault();                          // Cegah submit bawaan browser
                handleAddRoleSubmission(e.target);           // Kirim via AJAX
            }
        });

        // ─── RESET FORM SAAT MODAL DITUTUP ───
        // 'hidden.bs.modal' = event Bootstrap yang dipicu setelah modal selesai tertutup
        // Reset form agar saat dibuka lagi, semua field kosong (tidak berisi data sebelumnya)
        const addRoleModal = document.getElementById('addRoleModal');
        if (addRoleModal) {
            addRoleModal.addEventListener('hidden.bs.modal', function() {
                const form = document.getElementById('addRoleForm');
                if (form) {
                    form.reset();  // Reset semua input ke nilai default
                    // Pastikan checkbox "Select All" juga di-uncheck
                    const selectAll = document.getElementById('selectAll');
                    if (selectAll) selectAll.checked = false;
                }
            });
        }
    });

    // ─────────────────────────────────────────────────────────
    // HANDLE SELECT ALL — Centang/Uncentang Semua Checkbox
    // ─────────────────────────────────────────────────────────
    // Saat checkbox "Select All" dicentang → semua permission dicentang
    // Saat checkbox "Select All" di-uncheck → semua permission di-uncheck
    //
    // Parameter:
    //   selectAllCheckbox (HTMLInputElement) — Checkbox "Select All"
    // ─────────────────────────────────────────────────────────
    function handleSelectAllChange(selectAllCheckbox) {
        const isChecked = selectAllCheckbox.checked;  // True jika dicentang
        const form = document.getElementById('addRoleForm');
        if (!form) return;

        // Cari semua checkbox permission di dalam form
        const checkboxes = form.querySelectorAll('.permission-checkbox');
        // Set semua checkbox sesuai status "Select All"
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = isChecked;
        });
    }

    // ─────────────────────────────────────────────────────────
    // UPDATE SELECT ALL STATE — Perbarui Status Checkbox Select All
    // ─────────────────────────────────────────────────────────
    // Dipanggil setiap kali checkbox permission individual berubah.
    // Mengatur status checkbox "Select All":
    // - ✓ Centang penuh   → jika SEMUA checkbox permission tercentang
    // - ☐ Kosong          → jika TIDAK ADA checkbox yang tercentang
    // - ▣ Indeterminate   → jika SEBAGIAN checkbox tercentang (garis horizontal)
    //
    // Apa itu 'indeterminate'?
    // State ketiga checkbox (selain checked/unchecked) yang menunjukkan
    // "sebagian tercentang". Hanya bisa di-set via JavaScript, tidak bisa via HTML.
    // ─────────────────────────────────────────────────────────
    function updateSelectAllState() {
        const selectAllCheckbox = document.getElementById('selectAll');
        if (!selectAllCheckbox) return;

        // Hitung total checkbox dan yang tercentang
        const allCheckboxes = document.querySelectorAll('#addRoleForm .permission-checkbox');
        const checkedCheckboxes = document.querySelectorAll('#addRoleForm .permission-checkbox:checked');

        if (allCheckboxes.length === 0) return;

        // Set status berdasarkan perbandingan jumlah
        selectAllCheckbox.checked = allCheckboxes.length === checkedCheckboxes.length;
        selectAllCheckbox.indeterminate = checkedCheckboxes.length > 0 && checkedCheckboxes.length < allCheckboxes.length;
    }

    // ─────────────────────────────────────────────────────────
    // HANDLE ADD ROLE SUBMISSION — Kirim Form via AJAX
    // ─────────────────────────────────────────────────────────
    // Mengirim data role baru (nama role + daftar permission)
    // ke server via AJAX POST.
    //
    // Data yang dikirim:
    // - role_name → Nama role baru (misal: "KASIR")
    // - csrfmiddlewaretoken → Token CSRF untuk keamanan
    // - perms[module][action] → Permission level modul (misal: perms[produk][view])
    // - perms[module][subs][sub_code][action] → Permission level sub-modul
    //
    // Parameter:
    //   form (HTMLFormElement) — Form yang di-submit
    // ─────────────────────────────────────────────────────────
    function handleAddRoleSubmission(form) {
        // Ambil nilai nama role dari input
        const roleNameInput = document.getElementById('role_name');
        const roleName = roleNameInput ? roleNameInput.value.trim() : '';
        const submitBtn = form.querySelector('button[type="submit"]');

        // ─── VALIDASI ───
        if (!roleName) {
            showToast('error', 'Nama role harus diisi!');
            return;
        }

        if (!submitBtn) return;

        // Simpan teks asli tombol untuk di-restore nanti
        const originalBtnText = submitBtn.innerHTML;

        // ─── LOADING STATE ───
        // Disable tombol dan tampilkan spinner untuk mencegah double-submit
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Menyimpan...';

        // ─── CSRF TOKEN ───
        // Ambil token CSRF dari hidden input yang di-generate oleh Django
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfInput ? csrfInput.value : '';

        // ─── BANGUN DATA FORM ───
        // Menggunakan URLSearchParams untuk encoding data form
        // Format: key=value&key2=value2 (application/x-www-form-urlencoded)
        const data = new URLSearchParams();
        data.append('role_name', roleName);
        data.append('csrfmiddlewaretoken', csrfToken);

        // ─── KUMPULKAN PERMISSION LEVEL MODUL ───
        // Checkbox dengan class 'module-perm' = permission untuk modul utama
        // Format nama checkbox: perms[module][action]
        // Contoh: perms[produk][view], perms[produk][create]
        const moduleCheckboxes = form.querySelectorAll('.module-perm:checked');
        moduleCheckboxes.forEach(function(checkbox) {
            if (checkbox.name) {
                data.append(checkbox.name, 'on');  // 'on' = standar HTML untuk checkbox tercentang
            }
        });

        // ─── KUMPULKAN PERMISSION LEVEL SUB-MODUL ───
        // Checkbox dengan class 'sub-perm' = permission untuk sub-modul
        // Format nama checkbox: perms[module][subs][sub_code][action]
        // Contoh: perms[produk][subs][kategori][view]
        const subCheckboxes = form.querySelectorAll('.sub-perm:checked');
        subCheckboxes.forEach(function(checkbox) {
            if (checkbox.name) {
                data.append(checkbox.name, 'on');
            }
        });

        // ─── KIRIM AJAX POST ───
        fetch('/access/roles/ajax/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',  // Format encoding data
                'X-CSRFToken': csrfToken,                              // Header CSRF
            },
            body: data.toString()  // Konversi URLSearchParams ke string
        })
        .then(function(response) {
            return response.json();  // Parse response JSON dari server
        })
        .then(function(responseData) {
            if (responseData.success) {
                // ─── BERHASIL ───
                showToast('success', responseData.message || 'Role berhasil ditambahkan!');

                // Tutup modal Bootstrap
                var modalEl = document.getElementById('addRoleModal');
                var modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();

                // Reload halaman setelah 1 detik agar role baru muncul di tabel
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            } else {
                // ─── GAGAL (dari server) ───
                showToast('error', responseData.message || 'Gagal menambahkan role!');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        })
        .catch(function(error) {
            // ─── ERROR JARINGAN ───
            console.error('Error:', error);
            showToast('error', 'Terjadi kesalahan pada server!');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        });
    }

    // ─────────────────────────────────────────────────────────
    // SHOW TOAST — Tampilkan Notifikasi Pop-up
    // ─────────────────────────────────────────────────────────
    // Menggunakan SweetAlert2 untuk menampilkan notifikasi toast
    // di pojok kanan atas halaman.
    //
    // Parameter:
    //   type (string) — Tipe: 'success' (berhasil) atau 'error' (gagal)
    //   message (string) — Pesan yang ditampilkan
    // ─────────────────────────────────────────────────────────
    function showToast(type, message) {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                icon: type === 'success' ? 'success' : 'error',
                title: type === 'success' ? 'Sukses!' : 'Error!',
                text: message,
                timer: 3000,              // Otomatis tutup setelah 3 detik
                showConfirmButton: false,  // Tanpa tombol OK
                toast: true,               // Mode toast (kecil, di pojok)
                position: 'top-end'        // Posisi: pojok kanan atas
            });
        } else {
            // Fallback jika SweetAlert2 tidak tersedia
            alert(message);
        }
    }

})();  // Akhir IIFE
