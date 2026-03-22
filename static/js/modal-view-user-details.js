/**
 * ==========================================================================
 *  VIEW USER DETAILS MODAL — Tampilkan Detail User di Modal
 * ==========================================================================
 *  File ini menangani pemuatan dan penampilan detail informasi user
 *  saat tombol "View Details" diklik di tabel user.
 *
 *  Fitur:
 *  1. Load data user dari server via AJAX
 *  2. Fallback ke data DOM jika endpoint AJAX tidak tersedia
 *  3. Populate modal dengan informasi lengkap user
 *
 *  Alur kerja:
 *  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
 *  │ User klik    │    │ AJAX GET     │    │ Populate     │
 *  │ tombol       │───→│ /user-mgmt/  │───→│ modal dengan │
 *  │ "View"       │    │ detail/{id}/ │    │ data user    │
 *  └──────────────┘    └──────────────┘    └──────────────┘
 *                              │ (gagal?)
 *                              ▼
 *                      ┌──────────────┐
 *                      │ Fallback:    │
 *                      │ ambil data   │
 *                      │ dari tabel   │
 *                      │ HTML (DOM)   │
 *                      └──────────────┘
 *
 *  Terhubung dengan:
 *  - templates/access/roles.html → Template yang memuat modal ini
 *  - apps/user_management/views.py → Endpoint AJAX detail user
 *
 *  Dependensi:
 *  - Bootstrap 5 (Modal) → Popup detail user
 * ==========================================================================
 */

// IIFE — membungkus kode agar variabel tidak bocor ke scope global
(function() {
    'use strict';  // Mode ketat JavaScript

    // ═══════════════════════════════════════════════════════
    // INISIALISASI — Setup event listener setelah DOM siap
    // ═══════════════════════════════════════════════════════
    document.addEventListener('DOMContentLoaded', function() {
        initializeViewUserDetailsModal();
    });

    // ─────────────────────────────────────────────────────────
    // INISIALISASI MODAL VIEW USER DETAILS
    // ─────────────────────────────────────────────────────────
    // Memasang event listener pada modal agar saat dibuka,
    // data user otomatis dimuat berdasarkan user ID.
    //
    // Event 'show.bs.modal':
    // - Dipicu saat modal AKAN ditampilkan (sebelum animasi)
    // - event.relatedTarget = tombol yang memicu modal
    // - User ID diambil dari atribut data-user-id di tombol
    // ─────────────────────────────────────────────────────────
    function initializeViewUserDetailsModal() {
        const modal = document.getElementById('viewUserDetailsModal');
        if (!modal) return;  // Skip jika modal tidak ada di halaman

        // Pasang listener untuk event modal dibuka
        modal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;  // Tombol yang diklik
            if (button) {
                // Ambil user ID dari atribut data-user-id
                // Contoh HTML: <button data-user-id="5">View Details</button>
                const userId = button.getAttribute('data-user-id');
                if (userId) {
                    loadUserData(userId);  // Muat data user dari server
                }
            }
        });
    }

    // ─────────────────────────────────────────────────────────
    // LOAD USER DATA — Muat Data User dari Server via AJAX
    // ─────────────────────────────────────────────────────────
    // Mengambil data user dari endpoint AJAX Django.
    // Jika endpoint tidak tersedia (404/500), fallback ke
    // pengambilan data dari DOM tabel HTML.
    //
    // Alur:
    // 1. Tampilkan "Loading..." di semua field modal
    // 2. Fetch data dari /user-management/detail/{userId}/ajax/
    // 3. Jika berhasil → populate modal dengan data server
    // 4. Jika gagal → ambil data dari tabel HTML (fallback)
    //
    // Parameter:
    //   userId (string) — ID user di database
    // ─────────────────────────────────────────────────────────
    function loadUserData(userId) {
        console.log('Loading user data for ID:', userId);

        // ─── TAMPILKAN LOADING STATE ───
        // Set semua field modal ke "Loading..." sementara data diambil
        document.getElementById('viewUserFullName').textContent = 'Loading...';
        document.getElementById('viewUserUsername').textContent = '-';
        document.getElementById('viewUserEmail').textContent = '-';
        document.getElementById('viewUserPermissions').innerHTML = '<span class="badge bg-label-secondary">Loading...</span>';

        // ─── FETCH DATA VIA AJAX ───
        // Template literal `${}` menyisipkan userId ke URL
        fetch(`/user-management/detail/${userId}/ajax/`)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    // ─── ENDPOINT TIDAK TERSEDIA ───
                    // response.ok = false jika status code bukan 200-299
                    // Fallback: ambil data dari DOM tabel HTML
                    populateFromDOM(userId);
                    return null;  // Return null agar .then() berikutnya bisa cek
                }
                return response.json();  // Parse JSON jika berhasil
            })
            .then(data => {
                if (data && data.success) {
                    // ─── DATA DARI SERVER BERHASIL ───
                    populateModal(data.user);
                } else if (data === null) {
                    // Sudah di-handle di populateFromDOM()
                    console.log('Populated from DOM data');
                } else {
                    // Server mengembalikan success=false
                    console.error('Failed to load user data:', data.message);
                    populateFromDOM(userId);
                }
            })
            .catch(error => {
                // ─── ERROR JARINGAN ───
                console.error('Error loading user data:', error);
                populateFromDOM(userId);  // Fallback ke DOM
            });
    }

    // ─────────────────────────────────────────────────────────
    // POPULATE FROM DOM — Ambil Data User dari Tabel HTML
    // ─────────────────────────────────────────────────────────
    // Fallback: Jika endpoint AJAX tidak tersedia, data user
    // diambil langsung dari baris (<tr>) tabel HTML yang ada
    // di halaman.
    //
    // Cara kerja:
    // 1. Cari baris tabel (<tr>) yang memiliki data-user-id yang cocok
    // 2. Baca teks dari setiap sel (<td>) di baris tersebut
    // 3. Isi field modal dengan data yang ditemukan
    //
    // Parameter:
    //   userId (string) — ID user yang dicari
    // ─────────────────────────────────────────────────────────
    function populateFromDOM(userId) {
        console.log('Populating modal from DOM data');

        // Cari baris tabel yang sesuai dengan userId
        // Strategi 1: Cari <tr> dengan atribut data-user-id
        // Strategi 2: Cari <a> dengan data-user-id dan ambil baris induknya
        const userRow = document.querySelector(`tr[data-user-id="${userId}"]`) ||
                       document.querySelector(`a[data-user-id="${userId}"]`).closest('tr');

        if (userRow) {
            // ─── EKSTRAK DATA DARI SEL TABEL ───
            // Setiap sel (<td>) berisi data user:
            // cells[0] = No/ID, cells[1] = Username, cells[2] = Email, dst
            const cells = userRow.querySelectorAll('td');

            // Operator ?. (optional chaining) → mencegah error jika cells[n] undefined
            // Contoh: cells[1]?.textContent → null jika cells[1] tidak ada
            const username = cells[1]?.textContent.trim() || 'Unknown';
            const email = cells[2]?.textContent.trim() || 'N/A';
            const role = cells[3]?.textContent.trim() || 'User';
            const status = cells[4]?.querySelector('.badge')?.textContent.trim() || 'Unknown';

            // ─── ISI FIELD MODAL ───
            document.getElementById('viewUserFullName').textContent = username;
            document.getElementById('viewUserUsername').textContent = username.toLowerCase().replace(' ', '');
            document.getElementById('viewUserEmail').textContent = email;
            document.getElementById('viewUserPhone').textContent = 'N/A';
            document.getElementById('viewUserJoined').textContent = new Date().toLocaleDateString();
            document.getElementById('viewUserRole').textContent = role;
            document.getElementById('viewUserStatus').textContent = status;
            document.getElementById('viewUserLastLogin').textContent = 'N/A';

            // ─── STATUS BADGE ───
            // Warna badge berdasarkan status aktif/tidak
            const statusBadge = document.getElementById('viewUserStatusBadge');
            statusBadge.textContent = status;
            statusBadge.className = status === 'Active' ? 'badge bg-label-success mt-2' : 'badge bg-label-secondary mt-2';

            // ─── PERMISSIONS (PLACEHOLDER) ───
            // Menampilkan badge permission placeholder
            // Karena data DOM tidak menyertakan detail permission
            document.getElementById('viewUserPermissions').innerHTML = `
                <span class="badge bg-label-primary">View</span>
                <span class="badge bg-label-info">Edit</span>
                <span class="badge bg-label-warning">Create</span>
            `;
        } else {
            console.error('Could not find user row for ID:', userId);
        }
    }

    // ─────────────────────────────────────────────────────────
    // POPULATE MODAL — Isi Modal dengan Data dari Server
    // ─────────────────────────────────────────────────────────
    // Mengisi semua field modal dengan data lengkap user dari server.
    // Data server lebih lengkap dari data DOM (termasuk avatar,
    // phone, permissions, dll).
    //
    // Parameter:
    //   user (Object) — Objek user dari response JSON server:
    //     {
    //       username: "john",
    //       full_name: "John Doe",
    //       email: "john@example.com",
    //       phone: "08123456789",
    //       avatar: "/media/avatars/john.jpg",
    //       role: "Admin",
    //       is_active: true,
    //       date_joined: "2024-01-15",
    //       last_login: "2024-02-19",
    //       permissions: ["View Produk", "Edit Produk", ...]
    //     }
    // ─────────────────────────────────────────────────────────
    function populateModal(user) {
        console.log('Populating modal with user data:', user);

        // ─── INFORMASI DASAR ───
        document.getElementById('viewUserFullName').textContent = user.full_name || user.username;
        document.getElementById('viewUserUsername').textContent = user.username;

        // ─── AVATAR (Foto Profil) ───
        const avatarEl = document.getElementById('viewUser Avatar');
        if (user.avatar) {
            // Jika user punya foto avatar → tampilkan gambar
            avatarEl.innerHTML = `<img src="${user.avatar}" alt="${user.username}" class="rounded-circle">`;
        } else {
            // Jika tidak punya avatar → tampilkan huruf awal nama
            // Contoh: "John" → "J" (dalam lingkaran berwarna)
            const initial = user.username.charAt(0).toUpperCase();
            avatarEl.innerHTML = `<span class="avatar-initial rounded-circle bg-label-primary">${initial}</span>`;
        }

        // ─── INFORMASI PERSONAL ───
        document.getElementById('viewUserEmail').textContent = user.email || 'N/A';
        document.getElementById('viewUserPhone').textContent = user.phone || 'N/A';
        document.getElementById('viewUserJoined').textContent = user.date_joined || 'N/A';

        // ─── INFORMASI AKUN ───
        document.getElementById('viewUserRole').textContent = user.role || 'User';
        document.getElementById('viewUserStatus').textContent = user.is_active ? 'Active' : 'Inactive';
        document.getElementById('viewUserLastLogin').textContent = user.last_login || 'Never';

        // ─── STATUS BADGE ───
        // Warna badge berubah sesuai status:
        // Active → hijau (bg-label-success)
        // Inactive → abu-abu (bg-label-secondary)
        const statusBadge = document.getElementById('viewUserStatusBadge');
        statusBadge.textContent = user.is_active ? 'Active' : 'Inactive';
        statusBadge.className = user.is_active ? 'badge bg-label-success mt-2' : 'badge bg-label-secondary mt-2';

        // ─── PERMISSIONS (Hak Akses) ───
        // Tampilkan daftar permission sebagai badge warna-warni
        if (user.permissions && user.permissions.length > 0) {
            // Map setiap permission ke HTML badge
            const permissionsHTML = user.permissions.map(perm =>
                `<span class="badge bg-label-primary">${perm}</span>`
            ).join(' ');
            document.getElementById('viewUserPermissions').innerHTML = permissionsHTML;
        } else {
            // Tidak ada permission khusus
            document.getElementById('viewUserPermissions').innerHTML = '<span class="badge bg-label-secondary">No specific permissions</span>';
        }
    }

})();  // Akhir IIFE
