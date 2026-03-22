/**
 * ==========================================================================
 *  APP ACCESS ROLES - Inisialisasi DataTables & Interaksi UI
 * ==========================================================================
 *  File ini menangani inisialisasi komponen UI di halaman Role & User
 *  pada modul Access Control (Hak Akses).
 *
 *  Fungsi utama:
 *  1. initializeUsersDatatable() → Inisialisasi tabel user dengan DataTables
 *  2. initializeTooltips() → Aktifkan Bootstrap tooltip di halaman
 *
 *  Apa itu DataTables?
 *  DataTables adalah plugin jQuery yang mengubah tabel HTML biasa menjadi
 *  tabel interaktif dengan fitur: sorting, searching, pagination, dll.
 *
 *  Terhubung dengan:
 *  - templates/access/roles.html → Template halaman role yang memuat file ini
 *  - jQuery & DataTables plugin → Library eksternal yang harus dimuat duluan
 *  - Bootstrap 5 → Untuk komponen tooltip
 * ==========================================================================
 */

// IIFE — membungkus semua kode agar variabel tidak bocor ke scope global
(function() {
    'use strict';  // Mode ketat JavaScript

    // ═══════════════════════════════════════════════════════
    // INISIALISASI — Jalankan setelah DOM selesai dimuat
    // ═══════════════════════════════════════════════════════
    document.addEventListener('DOMContentLoaded', function() {
        initializeUsersDatatable();  // Setup tabel user dengan DataTables
        initializeTooltips();        // Aktifkan semua tooltip di halaman
    });

    // ─────────────────────────────────────────────────────────
    // INISIALISASI DATATABLES UNTUK TABEL USER
    // ─────────────────────────────────────────────────────────
    // Mengubah tabel HTML biasa menjadi tabel interaktif dengan:
    // - Pencarian (search box)
    // - Sorting per kolom (klik header untuk urutkan)
    // - Pagination (halaman per 10 data)
    // - Bahasa Indonesia untuk semua label
    //
    // Catatan:
    // - $(table).DataTable() adalah syntax jQuery — $() membungkus elemen DOM
    // - DataTable() adalah method dari plugin DataTables jQuery
    // ─────────────────────────────────────────────────────────
    function initializeUsersDatatable() {
        // Cari elemen tabel dengan class CSS 'datatables-users'
        const table = document.querySelector('.datatables-users');
        if (!table) return;  // Skip jika tabel tidak ada di halaman

        // Inisialisasi DataTables dengan konfigurasi
        $(table).DataTable({
            responsive: true,  // Tabel otomatis responsif (sembunyikan kolom di layar kecil)

            // ─── BAHASA INDONESIA ───
            // Menerjemahkan semua label bawaan DataTables ke Bahasa Indonesia
            language: {
                search: "Cari:",                                                   // Label search box
                lengthMenu: "Tampilkan _MENU_ users",                             // Label dropdown jumlah data
                info: "Menampilkan _START_ sampai _END_ dari _TOTAL_ users",      // Info halaman
                infoEmpty: "Tidak ada data",                                       // Pesan jika tabel kosong
                infoFiltered: "(difilter dari _MAX_ total users)",                 // Info saat difilter
                zeroRecords: "User tidak ditemukan",                               // Pesan jika pencarian tidak menemukan
                emptyTable: "Tidak ada user yang tersedia",                        // Pesan tabel kosong
                paginate: {
                    first: "Pertama",       // Tombol halaman pertama
                    last: "Terakhir",       // Tombol halaman terakhir
                    next: "Selanjutnya",    // Tombol halaman berikutnya
                    previous: "Sebelumnya"  // Tombol halaman sebelumnya
                }
            },

            // Sorting default: kolom pertama (index 0), urut ascending (A-Z)
            order: [[0, 'asc']],

            // Jumlah baris per halaman (default 10)
            pageLength: 10,

            // Konfigurasi per-kolom
            columnDefs: [
                {
                    targets: 4,          // Kolom ke-5 (index 4) = kolom "Actions"
                    orderable: false,    // Tidak bisa di-sort (karena berisi tombol, bukan data)
                    searchable: false    // Tidak ikut dalam pencarian
                }
            ]
        });
    }

    // ─────────────────────────────────────────────────────────
    // INISIALISASI BOOTSTRAP TOOLTIPS
    // ─────────────────────────────────────────────────────────
    // Mengaktifkan tooltip Bootstrap di semua elemen yang memiliki
    // atribut data-bs-toggle="tooltip".
    //
    // Tooltip = teks kecil yang muncul saat hover di atas elemen
    // Contoh: hover di atas ikon edit → muncul teks "Edit User"
    //
    // Bootstrap tooltip harus diinisialisasi secara manual via JS
    // (tidak otomatis aktif hanya dengan menambahkan atribut HTML)
    // ─────────────────────────────────────────────────────────
    function initializeTooltips() {
        // Cari semua elemen dengan atribut data-bs-toggle="tooltip"
        // [].slice.call() → konversi NodeList ke Array (agar bisa pakai .map())
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

        // Buat instance Bootstrap Tooltip untuk setiap elemen
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

})();  // Akhir IIFE