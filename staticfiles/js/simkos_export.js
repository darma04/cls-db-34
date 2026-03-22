/**
 * ==========================================================================
 *  SIMKOS EXPORT UTILITIES - Versi 3.0
 *  Export Excel & PDF dengan DataTables API, Kop Surat, Baris Ringkasan
 *  yang TEPAT SEJAJAR di kolom nominal yang benar.
 * ==========================================================================
 *
 *  CARA PAKAI DI SETIAP HALAMAN:
 *
 *  1. Include di vendor_js:
 *     <script src="{% static 'js/simkos_export.js' %}"></script>
 *
 *  2. Definisikan variabel konfigurasi:
 *     var EXCEL_INFO = { name, address, phone, email, copyright };
 *     var PDF_INFO   = { name, address, phone, email, copyright };
 *     // FOOTER_DATA: key = indeks kolom DataTables (0-based, termasuk kolom Aksi),
 *     //              value = nominal ANGKA (akan diformat otomatis menjadi Rp)
 *     var FOOTER_DATA  = { 3: 5000000 };   // total di kolom indeks ke-3
 *     var FOOTER_LABEL = 'RINGKASAN (10 Tagihan | Belum: 3 | Lunas: 7)';
 *
 *  3. Panggil fungsi:
 *     function exportToExcel() { SimkosExport.buildExcel('#tabelId', EXCEL_INFO, FOOTER_DATA, FOOTER_LABEL, 'JUDUL', 'NamaFile'); }
 *     function exportToPDF()   { SimkosExport.buildPDF('#tabelId', PDF_INFO,   FOOTER_DATA, FOOTER_LABEL, 'JUDUL', 'NamaFile'); }
 *     function toggleColumns() { SimkosExport.toggleColumns('#tabelId'); }
 *
 * ==========================================================================
 */

var SimkosExport = (function () {
    'use strict';

    // ── FORMAT RUPIAH ─────────────────────────────────────────────────────────
    /**
     * Format angka menjadi string Rupiah Indonesia.
     * Contoh: 10400000 → "Rp 10.400.000"
     * @param {number|string} value
     * @returns {string}
     */
    function _formatRupiah(value) {
        var num = parseFloat(String(value).replace(/[^\d.-]/g, ''));
        if (isNaN(num)) return String(value); // biarkan apa adanya jika bukan angka
        return 'Rp ' + num.toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    }

    /**
     * Format angka biasa (tanpa prefix Rp).
     * Contoh: 11 → "11", 1500 → "1.500"
     * @param {number|string} value
     * @returns {string}
     */
    function _formatNumber(value) {
        var num = parseFloat(String(value).replace(/[^\d.-]/g, ''));
        if (isNaN(num)) return String(value);
        return num.toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    }

    /**
     * Cek apakah nilai tampak seperti nominal uang (bisa berisi "Rp", titik, koma, angka)
     * Angka 0 dianggap valid!
     * @param {string} str
     * @returns {boolean}
     */
    function _isMoneyLike(str) {
        var s = String(str).trim();
        return /^(Rp[\s\.]?)?[\d.,]+$/.test(s) || s === '0';
    }

    /**
     * Cek apakah kolom tertentu adalah kolom nominal uang.
     * @param {number}      colIdx       - Indeks kolom DataTables
     * @param {Array|null}  moneyColumns - Array indeks kolom yang merupakan nominal uang. Null=semua dianggap uang.
     * @returns {boolean}
     */
    function _isMoneyColumn(colIdx, moneyColumns) {
        if (!moneyColumns || !Array.isArray(moneyColumns)) return true; // default: semua diformat Rp (backward compatible)
        return moneyColumns.indexOf(colIdx) !== -1;
    }

    /**
     * Format nilai footer sesuai tipe kolom (uang atau angka biasa).
     * @param {*}           rawVal       - Nilai mentah
     * @param {number}      colIdx       - Indeks kolom
     * @param {Array|null}  moneyColumns - Kolom mana yang nominal uang
     * @returns {string}
     */
    function _formatFooterValue(rawVal, colIdx, moneyColumns) {
        var str = String(rawVal);
        if (_isMoneyColumn(colIdx, moneyColumns)) {
            return _isMoneyLike(str) ? _formatRupiah(rawVal) : str;
        } else {
            // Bukan kolom uang — tampilkan sebagai angka biasa tanpa Rp
            return _isMoneyLike(str) ? _formatNumber(rawVal) : str;
        }
    }

    // ── TOGGLE KOLOM ─────────────────────────────────────────────────────────
    /**
     * Toggle visibility kolom DataTable berdasarkan checkbox .column-checkbox.
     * Menggunakan new $.fn.dataTable.Api() agar TIDAK re-initialize tabel.
     * @param {string} tableId - Selector ID tabel, mis: '#pembayaranTable'
     */
    function toggleColumns(tableId) {
        if (typeof $ === 'undefined' || typeof $.fn.dataTable === 'undefined') {
            console.error('SimkosExport: jQuery DataTables belum dimuat!');
            return;
        }
        try {
            var tableApi = new $.fn.dataTable.Api(tableId);
            document.querySelectorAll('.column-checkbox').forEach(function (cb) {
                tableApi.column(parseInt(cb.value)).visible(cb.checked);
            });
        } catch (e) {
            console.error('SimkosExport.toggleColumns error:', e);
        }
    }

    // ── AMBIL KOLOM VISIBLE ───────────────────────────────────────────────────
    /**
     * Ambil daftar kolom yang visible dari DataTable (kecuali kolom "Aksi").
     * @param {string} tableId
     * @returns {Array} [{index, text}]
     */
    function _getVisibleColumns(tableId) {
        var tableApi = new $.fn.dataTable.Api(tableId);
        var cols = [];
        tableApi.columns().every(function (index) {
            var headerNode = this.header();
            var headerText = headerNode ? headerNode.textContent.trim() : '';
            var lowerText = headerText.toLowerCase();
            // Skip kolom "Aksi", "Action", "Tindakan", atau header kosong dari export
            var isActionCol = (lowerText === 'aksi' || lowerText === 'action' || lowerText === 'tindakan' || lowerText === '');
            if (this.visible() && !isActionCol) {
                cols.push({ index: index, text: headerText });
            }
        });
        return cols;
    }

    // ── BANGUN BARIS RINGKASAN EXCEL ──────────────────────────────────────────
    /**
     * Bangun array sel baris ringkasan untuk Excel.
     * Algoritma:
     *  - Scan visibleColumns dari kiri ke kanan
     *  - Jika colIdx ada di footerData → tampilkan total (format Rupiah HANYA jika termasuk moneyColumns)
     *  - Jika tidak → kumpulkan kolom berurutan, jadikan satu colspan
     *                 Kolom span pertama (paling kiri) tampilkan footerLabel
     *
     * @param {Array}      visibleColumns - [{index, text}]
     * @param {Object}     footerData     - { colIdx: nilaiTotal } (colIdx = indeks DataTables asli)
     * @param {string}     footerLabel    - Teks label ringkasan
     * @param {Array|null} moneyColumns   - Indeks kolom yang merupakan nominal uang (Rp). Null=semua.
     * @returns {Array} [{text, span}]
     */
    function _buildSummaryRowExcel(visibleColumns, footerData, footerLabel, moneyColumns) {
        var cells = [];
        var labelPlaced = false;
        var ri = 0;

        while (ri < visibleColumns.length) {
            var colIdx = visibleColumns[ri].index;

            if (footerData && footerData[colIdx] !== undefined && footerData[colIdx] !== null && footerData[colIdx] !== '') {
                // Kolom ini punya total — format sesuai tipe (uang atau angka biasa)
                var rawVal = footerData[colIdx];
                var formatted = _formatFooterValue(rawVal, colIdx, moneyColumns);
                cells.push({ text: formatted, span: 1, align: 'right', isTotal: true });
                ri++;
            } else {
                // Kumpulkan kolom berurutan yang tidak punya total
                var spanCount = 0;
                var si = ri;
                while (
                    si < visibleColumns.length &&
                    (!footerData || footerData[visibleColumns[si].index] === undefined ||
                        footerData[visibleColumns[si].index] === null ||
                        footerData[visibleColumns[si].index] === '')
                ) {
                    spanCount++;
                    si++;
                }
                var label = !labelPlaced ? (footerLabel || 'RINGKASAN') : '';
                if (!labelPlaced && label) labelPlaced = true;
                cells.push({ text: label, span: spanCount, align: 'left', isTotal: false });
                ri += spanCount;
            }
        }
        return cells;
    }

    // ── BANGUN BARIS RINGKASAN PDF ────────────────────────────────────────────
    /**
     * Bangun array sel baris ringkasan untuk pdfMake.
     * @param {Array}      visibleColumns
     * @param {Object}     footerData
     * @param {string}     footerLabel
     * @param {Array|null} moneyColumns - Indeks kolom yang merupakan nominal uang (Rp). Null=semua.
     * @returns {Array} array pdfMake cell objects
     */
    function _buildSummaryRowPDF(visibleColumns, footerData, footerLabel, moneyColumns) {
        var summaryRow = [];
        var labelPlaced = false;
        var ri = 0;

        while (ri < visibleColumns.length) {
            var colIdx = visibleColumns[ri].index;

            if (footerData && footerData[colIdx] !== undefined && footerData[colIdx] !== null && footerData[colIdx] !== '') {
                var rawVal = footerData[colIdx];
                var formatted = _formatFooterValue(rawVal, colIdx, moneyColumns);
                summaryRow.push({
                    text: formatted,
                    bold: true,
                    fillColor: '#EEF0FF',
                    color: '#4B4EE6',
                    alignment: 'right'
                });
                ri++;
            } else {
                var spanCount = 0;
                var si = ri;
                while (
                    si < visibleColumns.length &&
                    (!footerData || footerData[visibleColumns[si].index] === undefined ||
                        footerData[visibleColumns[si].index] === null ||
                        footerData[visibleColumns[si].index] === '')
                ) {
                    spanCount++;
                    si++;
                }
                var label = !labelPlaced ? (footerLabel || 'RINGKASAN') : '';
                if (!labelPlaced && label) labelPlaced = true;

                var cell = {
                    text: label,
                    bold: true,
                    fillColor: '#EEF0FF',
                    color: '#5F61E6',
                    alignment: 'left'
                };
                if (spanCount > 1) {
                    cell.colSpan = spanCount;
                }
                summaryRow.push(cell);
                // Tambah sel kosong untuk colspan
                for (var k = 1; k < spanCount; k++) {
                    summaryRow.push({ text: '', fillColor: '#EEF0FF' });
                }
                ri += spanCount;
            }
        }
        return summaryRow;
    }

    // ── EXPORT EXCEL ──────────────────────────────────────────────────────────
    /**
     * Export data tabel ke file Excel (.xls) dengan kop surat perusahaan dan baris ringkasan.
     *
     * @param {string} tableId     - Selector tabel, mis: '#pembayaranTable'
     * @param {Object} info        - { name, address, phone, email, copyright }
     * @param {Object} footerData  - { colIdx: nilaiTotal } — indeks kolom DataTables asli
     * @param {string} footerLabel - Label ringkasan (mis: 'RINGKASAN (10 Tagihan)')
     * @param {string} title       - Judul dokumen
     * @param {string} filename    - Nama file tanpa ekstensi
     * @param {Array}  [moneyColumns] - Opsional. Indeks kolom yang merupakan nominal uang (format Rp).
     *                                 Jika tidak diberikan, SEMUA kolom numerik diformat Rp (backward compatible).
     */
    function buildExcel(tableId, info, footerData, footerLabel, title, filename, moneyColumns) {
        try {
            var tableEl = document.querySelector(tableId);
            if (!tableEl) { alert('Tabel tidak ditemukan!'); return; }
            if (typeof $ === 'undefined' || typeof $.fn.dataTable === 'undefined') {
                alert('DataTables belum dimuat!'); return;
            }

            var visibleColumns = _getVisibleColumns(tableId);
            var tableApi = new $.fn.dataTable.Api(tableId);
            var colCount = visibleColumns.length;

            if (colCount === 0) { alert('Tidak ada kolom yang tersedia untuk di-export!'); return; }

            var html = '<html xmlns:o="urn:schemas-microsoft-com:office:office"'
                + ' xmlns:x="urn:schemas-microsoft-com:office:excel"'
                + ' xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8">'
                + '<style>table{border-collapse:collapse;} th,td{font-family:Arial,sans-serif;font-size:9pt;}'
                + '.kop-judul{font-size:14pt;font-weight:bold;color:#5F61E6;}'
                + '.kop-info{font-size:9pt;color:#697A8D;}'
                + '.th-header{background-color:#696CFF;color:#FFFFFF;font-weight:bold;padding:6px;}'
                + '.td-data{padding:4px 6px;}'
                + '.td-summary{background-color:#EEF0FF;font-weight:bold;padding:4px 6px;color:#4B4EE6;}'
                + '.td-label{background-color:#EEF0FF;font-weight:bold;padding:4px 6px;color:#5F61E6;}'
                + '</style></head><body>';

            // ── KOP SURAT ──
            html += '<table border="0" style="margin-bottom:8px;width:100%;">';
            html += '<tr><td colspan="' + colCount + '" style="text-align:center;font-size:16pt;font-weight:bold;color:#5F61E6;border:none;">' + (info.name || 'SIMKOS') + '</td></tr>';
            html += '<tr><td colspan="' + colCount + '" style="text-align:center;font-size:9pt;color:#697A8D;border:none;">' + (info.address || '') + '</td></tr>';
            html += '<tr><td colspan="' + colCount + '" style="text-align:center;font-size:9pt;color:#697A8D;border:none;">Telp: ' + (info.phone || '-') + ' | Email: ' + (info.email || '-') + '</td></tr>';
            html += '<tr><td colspan="' + colCount + '" style="border:none;">&nbsp;</td></tr>';
            html += '</table>';

            // ── JUDUL & TANGGAL ──
            html += '<table border="0" style="margin-bottom:6px;">';
            html += '<tr><td colspan="' + colCount + '" style="font-size:12pt;font-weight:bold;color:#5F61E6;border:none;">' + (title || 'Laporan') + '</td></tr>';
            html += '<tr><td colspan="' + colCount + '" style="font-size:8pt;color:#697A8D;border:none;">Tanggal: '
                + new Date().toLocaleDateString('id-ID', { day: '2-digit', month: 'long', year: 'numeric' }) + '</td></tr>';
            html += '<tr><td colspan="' + colCount + '" style="border:none;">&nbsp;</td></tr>';
            html += '</table>';

            // ── TABEL DATA ──
            html += '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;width:100%;">';

            // Header
            html += '<thead><tr>';
            visibleColumns.forEach(function (col) {
                html += '<th style="background-color:#696CFF;color:#FFFFFF;font-weight:bold;padding:6px;white-space:nowrap;border:1px solid #DBDADE;">' + col.text + '</th>';
            });
            html += '</tr></thead><tbody>';

            // Baris data — SEMUA baris yang lolos filter DataTables (bukan hanya halaman aktif)
            // search:'applied' = hormati filter pencarian tapi export semua halaman
            tableApi.rows({ search: 'applied' }).every(function (rowIdx) {
                html += '<tr>';
                visibleColumns.forEach(function (col) {
                    var cellNode = tableApi.cell(rowIdx, col.index).node();
                    var text = cellNode ? cellNode.textContent.trim().replace(/\s+/g, ' ') : '';
                    var isRight = /^Rp[\s]/.test(text) || /^[\d.,]+$/.test(text);
                    html += '<td style="padding:4px 6px;border:1px solid #DBDADE;' + (isRight ? 'text-align:right;' : '') + '">' + text + '</td>';
                });
                html += '</tr>';
            });

            // ── BARIS RINGKASAN ──
            var hasFooter = footerData && Object.keys(footerData).length > 0;
            var summaryCells = _buildSummaryRowExcel(visibleColumns, hasFooter ? footerData : {}, footerLabel, moneyColumns);
            html += '<tr>';
            summaryCells.forEach(function (cell) {
                var style = cell.isTotal
                    ? 'background-color:#EEF0FF;font-weight:bold;color:#4B4EE6;text-align:right;padding:5px 6px;border:1px solid #DBDADE;'
                    : 'background-color:#EEF0FF;font-weight:bold;color:#5F61E6;text-align:left;padding:5px 6px;border:1px solid #DBDADE;';
                if (cell.span > 1) {
                    html += '<td colspan="' + cell.span + '" style="' + style + '">' + cell.text + '</td>';
                } else {
                    html += '<td style="' + style + '">' + cell.text + '</td>';
                }
            });
            html += '</tr>';

            html += '</tbody></table>';

            // ── FOOTER ──
            html += '<table border="0" style="margin-top:8px;width:100%;">';
            html += '<tr>';
            html += '<td style="font-size:8pt;color:#697A8D;border:none;">Dicetak pada: ' + new Date().toLocaleString('id-ID') + '</td>';
            html += '<td style="font-size:8pt;color:#697A8D;text-align:right;border:none;">' + (info.copyright || '') + '</td>';
            html += '</tr></table>';

            html += '</body></html>';

            var blob = new Blob(['\uFEFF' + html], { type: 'application/vnd.ms-excel;charset=utf-8' });
            var link = document.createElement('a');
            link.setAttribute('href', URL.createObjectURL(blob));
            link.setAttribute('download', (filename || 'Export') + '_' + new Date().toISOString().slice(0, 10) + '.xls');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

        } catch (err) {
            console.error('SimkosExport.buildExcel error:', err);
            alert('Terjadi kesalahan saat export Excel: ' + err.message);
        }
    }

    // ── EXPORT PDF ────────────────────────────────────────────────────────────
    /**
     * Export data tabel ke PDF menggunakan pdfMake, dengan kop surat dan baris ringkasan.
     *
     * @param {string} tableId     - Selector tabel
     * @param {Object} info        - { name, address, phone, email, copyright }
     * @param {Object} footerData  - { colIdx: nilaiTotal }
     * @param {string} footerLabel - Label ringkasan
     * @param {string} title       - Judul dokumen
     * @param {string} filename    - Nama file tanpa ekstensi
     * @param {Array}  [moneyColumns] - Opsional. Indeks kolom yang merupakan nominal uang (format Rp).
     */
    function buildPDF(tableId, info, footerData, footerLabel, title, filename, moneyColumns) {
        try {
            if (typeof pdfMake === 'undefined') {
                alert('pdfMake library tidak tersedia! Pastikan pdfmake.min.js sudah dimuat.');
                return;
            }
            var tableEl = document.querySelector(tableId);
            if (!tableEl) { alert('Tabel tidak ditemukan!'); return; }

            var visibleColumns = _getVisibleColumns(tableId);
            var tableApi = new $.fn.dataTable.Api(tableId);
            var colCount = visibleColumns.length;

            if (colCount === 0) { alert('Tidak ada kolom yang tersedia untuk di-export!'); return; }

            // ── HEADER KOLOM ──
            var headers = visibleColumns.map(function (col) {
                return {
                    text: col.text,
                    style: 'tableHeader',
                    fillColor: '#696CFF',
                    color: '#FFFFFF',
                    bold: true,
                    alignment: 'center'
                };
            });

            // ── DATA BARIS — semua baris yang lolos filter (bukan hanya halaman aktif) ──
            var body = [headers];
            tableApi.rows({ search: 'applied' }).every(function (rowIdx) {
                var row = [];
                visibleColumns.forEach(function (col) {
                    var cellNode = tableApi.cell(rowIdx, col.index).node();
                    var text = cellNode ? cellNode.textContent.trim().replace(/\s+/g, ' ') : '';
                    if (text.length > 80) { text = text.substring(0, 77) + '...'; }
                    // Alignment kanan untuk kolom yang mengandung "Rp" atau angka
                    var isRightAlign = /^Rp[\s]/.test(text) || /^[\d.,]+$/.test(text);
                    row.push({ text: text, alignment: isRightAlign ? 'right' : 'left' });
                });
                if (row.length > 0) body.push(row);
            });

            // ── BARIS RINGKASAN ──
            var hasFooter = footerData && Object.keys(footerData).length > 0;
            var summaryRow = _buildSummaryRowPDF(visibleColumns, hasFooter ? footerData : {}, footerLabel, moneyColumns);
            if (summaryRow.length > 0) body.push(summaryRow);

            // ── HITUNG LEBAR KOLOM ──
            // Auto widths agar pdfMake menghitung otomatis berdasarkan konten
            var colWidths = Array(colCount).fill('auto');

            var bodyLength = body.length;

            var docDefinition = {
                pageOrientation: 'landscape',
                pageSize: 'A4',
                pageMargins: [30, 110, 30, 55],

                // ── KOP SURAT DI HEADER PDF ──
                header: function (currentPage) {
                    return {
                        margin: [30, 12, 30, 0],
                        table: {
                            widths: ['*', 80],
                            body: [[
                                {
                                    border: [false, false, false, true],
                                    stack: [
                                        { text: info.name || 'SIMKOS', style: 'companyName' },
                                        { text: info.address || '', style: 'companyInfo' },
                                        { text: 'Telp: ' + (info.phone || '-') + ' | Email: ' + (info.email || '-'), style: 'companyInfo' }
                                    ]
                                },
                                {
                                    border: [false, false, false, true],
                                    stack: [
                                        { text: 'Hal. ' + currentPage, style: 'pageNumber', alignment: 'right' }
                                    ]
                                }
                            ]]
                        },
                        layout: {
                            hLineWidth: function (i, node) { return (i === node.table.body.length) ? 1 : 0; },
                            vLineWidth: function () { return 0; },
                            hLineColor: function () { return '#696CFF'; }
                        }
                    };
                },

                content: [
                    { text: title || 'Laporan', style: 'documentTitle', margin: [0, 0, 0, 2] },
                    {
                        text: 'Tanggal: ' + new Date().toLocaleDateString('id-ID', { day: '2-digit', month: 'long', year: 'numeric' }),
                        style: 'dateText',
                        margin: [0, 0, 0, 10]
                    },
                    {
                        table: {
                            headerRows: 1,
                            dontBreakRows: true,
                            widths: colWidths,
                            body: body
                        },
                        layout: {
                            fillColor: function (rowIndex) {
                                if (rowIndex === 0) return '#696CFF';            // Header biru
                                if (rowIndex === bodyLength - 1) return '#EEF0FF'; // Ringkasan biru muda
                                return (rowIndex % 2 === 0) ? '#F5F5F9' : null;    // Zebra stripe
                            },
                            hLineWidth: function () { return 0.5; },
                            vLineWidth: function () { return 0.5; },
                            hLineColor: function () { return '#DBDADE'; },
                            vLineColor: function () { return '#DBDADE'; },
                            paddingLeft: function () { return 4; },
                            paddingRight: function () { return 4; },
                            paddingTop: function () { return 3; },
                            paddingBottom: function () { return 3; }
                        }
                    }
                ],

                // ── FOOTER PDF ──
                footer: function (currentPage, pageCount) {
                    return {
                        margin: [30, 8, 30, 0],
                        columns: [
                            { text: 'Dicetak pada: ' + new Date().toLocaleString('id-ID'), style: 'footerText' },
                            {
                                text: (info.copyright || '') + '  |  Halaman ' + currentPage + ' dari ' + pageCount,
                                style: 'footerText',
                                alignment: 'right'
                            }
                        ]
                    };
                },

                styles: {
                    companyName:   { fontSize: 13, bold: true, color: '#5F61E6' },
                    companyInfo:   { fontSize: 8,  color: '#697A8D' },
                    pageNumber:    { fontSize: 8,  color: '#697A8D' },
                    documentTitle: { fontSize: 14, bold: true, color: '#5F61E6' },
                    dateText:      { fontSize: 9,  color: '#697A8D' },
                    tableHeader:   { bold: true, fontSize: 8, color: '#FFFFFF' },
                    footerText:    { fontSize: 7,  color: '#697A8D' }
                },
                defaultStyle: { fontSize: 7 }
            };

            pdfMake.createPdf(docDefinition).download((filename || 'Export') + '_' + new Date().toISOString().slice(0, 10) + '.pdf');

        } catch (err) {
            console.error('SimkosExport.buildPDF error:', err);
            alert('Terjadi kesalahan saat export PDF: ' + err.message);
        }
    }

    // ── PUBLIC API ────────────────────────────────────────────────────────────
    return {
        toggleColumns: toggleColumns,
        buildExcel:    buildExcel,
        buildPDF:      buildPDF,
        formatRupiah:  _formatRupiah   // expose untuk penggunaan di halaman jika perlu
    };

})();
