/**
 * ==========================================================================
 *  EXPORT UTILITIES - Fungsi Ekspor Tabel ke Excel (CSV) dan PDF
 * ==========================================================================
 *  File ini berisi 2 fungsi utilitas untuk mengekspor data tabel HTML
 *  ke format file yang bisa didownload:
 *
 *  1. exportTableToExcel() → Ekspor tabel ke file CSV (bisa dibuka di Excel)
 *  2. exportTableToPDF()   → Ekspor tabel ke file PDF (membutuhkan pdfMake)
 *
 *  Cara kerja:
 *  - Membaca data dari elemen <table> di halaman
 *  - Mengkonversi data ke format CSV atau PDF
 *  - Membuat file download otomatis di browser
 *
 *  Digunakan oleh:
 *  - Tombol "Export Excel" di halaman CRUD (produk, supplier, dll)
 *  - Tombol "Export PDF" di halaman laporan
 *
 *  Dependensi:
 *  - pdfMake library (hanya untuk fungsi PDF) — dimuat dari CDN/vendor
 * ==========================================================================
 */

/**
 * Ekspor tabel HTML ke file Excel (format CSV).
 *
 * Cara kerja:
 * 1. Cari elemen <table> berdasarkan ID
 * 2. Baca semua header (th) dan baris data (td)
 * 3. Konversi ke format CSV (Comma-Separated Values)
 * 4. Buat file dan trigger download otomatis di browser
 *
 * @param {string} tableId  - ID elemen tabel HTML (contoh: "produkTable")
 * @param {string} filename - Nama file yang didownload (tanpa ekstensi, contoh: "Daftar_Produk")
 */
function exportTableToExcel(tableId, filename) {
    try {
        // Cari elemen tabel berdasarkan ID
        const table = document.getElementById(tableId);
        if (!table) {
            alert('Tabel tidak ditemukan!');
            return;
        }

        // Array untuk menyimpan semua baris CSV
        let csv = [];

        // ─── AMBIL HEADER TABEL ───
        // Baca teks dari setiap <th> di <thead>
        const headerRow = table.querySelector('thead tr');
        if (headerRow) {
            const headers = [];
            headerRow.querySelectorAll('th').forEach(th => {
                // Escape tanda kutip ganda (") dengan menggandakannya ("")
                // Lalu bungkus dengan tanda kutip untuk menangani koma di dalam teks
                headers.push('"' + th.textContent.trim().replace(/"/g, '""') + '"');
            });
            csv.push(headers.join(','));  // Gabung header dengan koma sebagai pemisah
        }

        // ─── AMBIL DATA BARIS ───
        // Baca teks dari setiap <td> di <tbody>
        const tbody = table.querySelector('tbody');
        if (tbody) {
            tbody.querySelectorAll('tr').forEach(tr => {
                const cells = tr.querySelectorAll('td');
                if (cells.length === 0) return;  // Skip baris kosong

                // Skip baris "empty state" (baris dengan colspan yang menampilkan "Tidak ada data")
                if (cells.length === 1 && cells[0].colSpan > 1) return;

                const row = [];
                cells.forEach(td => {
                    // Bersihkan teks: hapus whitespace berlebih dan escape tanda kutip
                    let text = td.textContent.trim();
                    text = text.replace(/\s+/g, ' ').replace(/"/g, '""');
                    row.push('"' + text + '"');
                });
                csv.push(row.join(','));  // Gabung kolom dengan koma
            });
        }

        // ─── BUAT FILE DOWNLOAD ───
        // Gabung semua baris dengan newline
        const csvContent = csv.join('\n');

        // BOM (Byte Order Mark) UTF-8 — diperlukan agar Excel mengenali encoding UTF-8
        // Tanpa BOM, karakter Indonesia (é, ñ, dll) bisa rusak di Excel
        const BOM = '\uFEFF';

        // Buat Blob (file virtual di memori browser)
        const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' });

        // Buat elemen <a> tersembunyi untuk trigger download
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);  // Buat URL sementara untuk Blob

        link.setAttribute('href', url);
        link.setAttribute('download', filename + '.csv');  // Set nama file download
        link.style.visibility = 'hidden';                  // Sembunyikan elemen
        document.body.appendChild(link);                    // Tambahkan ke DOM
        link.click();                                       // Trigger download
        document.body.removeChild(link);                    // Hapus elemen setelah download

    } catch (error) {
        console.error('Export Excel error:', error);
        alert('Terjadi kesalahan saat export Excel: ' + error.message);
    }
}

/**
 * Ekspor tabel HTML ke file PDF.
 *
 * Cara kerja:
 * 1. Cari elemen <table> berdasarkan ID
 * 2. Baca header dan data dari tabel
 * 3. Buat definisi dokumen PDF (layout, style, footer)
 * 4. Generate file PDF menggunakan library pdfMake
 * 5. Trigger download otomatis
 *
 * @param {string} tableId     - ID elemen tabel HTML
 * @param {string} filename    - Nama file PDF (tanpa ekstensi)
 * @param {string} title       - Judul dokumen PDF (ditampilkan di bagian atas)
 * @param {string} orientation - Orientasi halaman: 'portrait' (tegak) atau 'landscape' (mendatar)
 */
function exportTableToPDF(tableId, filename, title, orientation = 'landscape') {
    try {
        // Cek apakah library pdfMake tersedia
        // pdfMake harus dimuat sebelum fungsi ini dipanggil
        if (typeof pdfMake === 'undefined') {
            alert('pdfMake library tidak tersedia. Export PDF dibatalkan.');
            return;
        }

        // Cari elemen tabel
        const table = document.getElementById(tableId);
        if (!table) {
            alert('Tabel tidak ditemukan!');
            return;
        }

        // ─── AMBIL HEADER TABEL ───
        // Format header: teks putih dengan background ungu (#696CFF = warna primer tema)
        const headers = [];
        const headerRow = table.querySelector('thead tr');
        if (headerRow) {
            headerRow.querySelectorAll('th').forEach(th => {
                headers.push({
                    text: th.textContent.trim(),
                    style: 'tableHeader',           // Referensi ke style di bawah
                    fillColor: '#696CFF',           // Warna background header (ungu/primary)
                    color: '#FFFFFF',               // Warna teks (putih)
                    bold: true                      // Tebal
                });
            });
        }

        // ─── AMBIL DATA BARIS ───
        // Baris pertama = header, selanjutnya = data
        const body = [headers];
        const tbody = table.querySelector('tbody');
        if (tbody) {
            tbody.querySelectorAll('tr').forEach(tr => {
                const cells = tr.querySelectorAll('td');
                if (cells.length === 0) return;

                // Skip baris "empty state"
                if (cells.length === 1 && cells[0].colSpan > 1) return;

                const row = [];
                cells.forEach(td => {
                    let text = td.textContent.trim();
                    text = text.replace(/\s+/g, ' ');

                    // Potong teks yang terlalu panjang (max 100 karakter)
                    // Agar layout PDF tidak berantakan
                    if (text.length > 100) {
                        text = text.substring(0, 97) + '...';
                    }

                    row.push(text);
                });
                body.push(row);
            });
        }

        // ─── DEFINISI DOKUMEN PDF ───
        // Objek konfigurasi yang menentukan isi dan format PDF
        const docDefinition = {
            pageOrientation: orientation,          // Orientasi halaman: portrait/landscape
            pageMargins: [40, 60, 40, 60],         // Margin: [kiri, atas, kanan, bawah] dalam pt

            // Isi dokumen PDF (Array of content blocks)
            content: [
                // Judul dokumen
                {
                    text: title,
                    style: 'header',
                    margin: [0, 0, 0, 20]      // Margin bawah 20pt dari judul ke tabel
                },
                // Tabel data
                {
                    table: {
                        headerRows: 1,                                  // 1 baris header (di-repeat di halaman berikutnya)
                        widths: Array(headers.length).fill('auto'),     // Lebar kolom otomatis
                        body: body                                      // Data tabel
                    },
                    layout: {
                        // Warna latar baris: header ungu, baris genap abu-abu
                        fillColor: function (rowIndex) {
                            return (rowIndex === 0) ? '#696CFF' : ((rowIndex % 2 === 0) ? '#F5F5F9' : null);
                        },
                        // Garis tabel: tipis (0.5pt) dengan warna abu-abu terang
                        hLineWidth: function () { return 0.5; },
                        vLineWidth: function () { return 0.5; },
                        hLineColor: function () { return '#DBDADE'; },
                        vLineColor: function () { return '#DBDADE'; },
                    }
                },
                // Footer: tanggal cetak
                {
                    text: 'Dicetak pada: ' + new Date().toLocaleString('id-ID'),
                    style: 'footer',
                    margin: [0, 20, 0, 0]      // Margin atas 20pt dari tabel ke footer
                }
            ],

            // Definisi style yang digunakan di content
            styles: {
                header: {
                    fontSize: 18,
                    bold: true,
                    color: '#5F61E6'           // Warna judul (ungu sedikit lebih terang)
                },
                tableHeader: {
                    bold: true,
                    fontSize: 11,
                    color: '#FFFFFF'            // Teks header putih
                },
                footer: {
                    fontSize: 9,
                    italics: true,
                    color: '#697A8D'            // Warna abu-abu untuk footer
                }
            },

            // Style default untuk seluruh dokumen
            defaultStyle: {
                fontSize: 9                     // Ukuran font default 9pt (agar muat banyak kolom)
            }
        };

        // Generate dan download file PDF
        pdfMake.createPdf(docDefinition).download(filename + '.pdf');

    } catch (error) {
        console.error('Export PDF error:', error);
        alert('Terjadi kesalahan saat export PDF: ' + error.message);
    }
}
